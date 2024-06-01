import random
from typing import Dict, List, Tuple

import numpy as np
import sqlalchemy
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from icecream import ic
from pydantic import BaseModel
from sentence_transformers import CrossEncoder, SentenceTransformer
from sentence_transformers.util import cos_sim
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, sessionmaker

EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"

TABLE_NAME: str = "icons"
DATABASE_DIRECTORY: str = "../"
DATABASE_FILENAME: str = "tabler-icons.sqlite3"
DATABASE_URL = f"sqlite:///./{DATABASE_DIRECTORY}/{DATABASE_FILENAME}"

logseq_icon_search = FastAPI()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database model
class Icon(Base):
    __tablename__ = TABLE_NAME
    name = Column(String, primary_key=True)
    tags = Column(String)
    category = Column(String)
    glyph = Column(String)
    vector = Column(String)


# Pydantic model for icon keyword search request
class IconSearchRequest(BaseModel):
    search_string: str
    top_k: int = 5
    query_prompt: str = "Represent this sentence for searching relevant passages:"


class IconSearchResult(BaseModel):
    name: str
    tags: str
    glyph: str
    similarity_score: float


# Pydantic model for icon keyword search response
class IconSearchResponse(BaseModel):
    result: List[IconSearchResult]


# Pydantic model for the rerank input
class RerankInput(BaseModel):
    query: str
    documents: List[str]


# Pydantic model for a single rerank result
class RerankResult(BaseModel):
    corpus_id: int
    score: float
    text: str


# Pydantic model for the rerank response
class RerankResponse(BaseModel):
    results: List[RerankResult]


embedding_model = SentenceTransformer(EMBEDDING_MODEL)
rerank_model = CrossEncoder("mixedbread-ai/mxbai-rerank-base-v1")


def semantically_embed(model, text: str) -> List:
    """Generate a vector embedded with the semantic meaning of the text."""
    text_embedding = model.encode(text)
    return text_embedding


@logseq_icon_search.get(
    "/icon-search/{search_string}", response_model=IconSearchResponse
)
async def icon_search(
    search_string: str,
    top_k: int = 5,
    query_prompt: str = "Represent this sentence for searching relevant passages:",
    db: Session = Depends(get_db),
):
    search_query_embedding = semantically_embed(
        embedding_model, f"{query_prompt} {search_string}"
    )
    icons = db.query(Icon).all()

    icon_data = []
    for row in icons:
        icon_label = row.name
        icon_tags = row.tags
        icon_glyph = row.glyph
        icon_vector = np.frombuffer(row.vector, dtype=np.float32)
        similarity_score = cos_sim(search_query_embedding, icon_vector)
        icon_info = {
            "name": icon_label,
            "tags": icon_tags,
            "glyph": icon_glyph,
            "similarity_score": similarity_score.item(),
        }
        icon_data.append(icon_info)

    top_results = sorted(icon_data, key=lambda x: x["similarity_score"], reverse=True)[
        :top_k
    ]

    icon_results = [IconSearchResult(**result) for result in top_results]

    rerank_input_query = f"{query_prompt} {search_string}"
    rerank_input_documents = [result["keywords"] for result in top_results["result"]]
    rerank_results = rerank_model.rank(
        rerank_input_query,
        rerank_input_documents,
        return_documents=True,
        top_k=10,
    )

    return IconSearchResponse(result=icon_results)


@logseq_icon_search.get(
    "/reranked-search/{search_string}", response_model=RerankResponse
)
async def reranked_search(
    search_string: str,
    top_k: int = 5,
    query_prompt: str = "Represent this sentence for searching relevant passages:",
    db: Session = Depends(get_db),
):
    search_query_embedding = semantically_embed(
        embedding_model, f"{query_prompt} {search_string}"
    )
    icons = db.query(Icon).all()

    icon_data = []
    for row in icons:
        icon_label = row.name
        icon_tags = row.tags
        icon_glyph = row.glyph
        icon_vector = np.frombuffer(row.vector, dtype=np.float32)
        similarity_score = cos_sim(search_query_embedding, icon_vector)
        icon_info = {
            "name": icon_label,
            "tags": icon_tags,
            "glyph": icon_glyph,
            "similarity_score": similarity_score.item(),
        }
        icon_data.append(icon_info)

    n_search_results: int = top_k * 3
    top_search_results = sorted(
        icon_data, key=lambda x: x["similarity_score"], reverse=True
    )[:n_search_results]

    icon_results = [IconSearchResult(**result) for result in top_search_results]
    # icon_response = IconSearchResponse(result=icon_results) # I don't need this anymore I guess?

    rerank_input_data = {
        "query": f"{query_prompt} {search_string}",
        "documents": [result.tags for result in icon_results],
    }
    rerank_input = RerankInput(**rerank_input_data)
    # This is how the re-ranking model is normally used: rerank_results = rerank_model.rank(query, documents, return_documents=True, top_k=3)
    # Now we just need to pass the rerank input to the re-ranking model and get the results
    rerank_results = rerank_model.rank(
        rerank_input.query, rerank_input.documents, return_documents=True, top_k=top_k
    )
    logger.info(rerank_results)
    # Process the reranking results
    reranked_icon_results = []
    for rerank_result in rerank_results:
        # Find the corresponding icon result using the corpus_id
        corresponding_icon = icon_results[rerank_result["corpus_id"]]
        reranked_icon_results.append(
            IconSearchResult(
                name=corresponding_icon.name,
                tags=corresponding_icon.tags,
                glyph=corresponding_icon.glyph,
                similarity_score=rerank_result["score"],
            )
        )

    # Return the final results
    return IconSearchResponse(result=reranked_icon_results)
    """
    rerank_results_data = []
    for result in rerank_results:
        rerank_result_data = {
            "corpus_id": result.corpus_id,
            "score": result.score,
            "text": result.text,
        }
        rerank_results_data.append(rerank_result_data)

    # Sort reranked results by score
    top_reranked_results = sorted(
        rerank_results_data, key=lambda x: x["score"], reverse=True
    )[:top_k]
    rerank_results = [RerankResult(**result) for result in top_reranked_results]
    return RerankResponse(results=rerank_results)
    """


if __name__ == "__main__":

    uvicorn.run(logseq_icon_search, host="0.0.0.0", port=8666)
