from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Tuple, Dict
import random
import numpy as np
from icecream import ic
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"

TABLE_NAME: str = "icons"
DATABASE_DIRECTORY: str = "databases"
DATABASE_FILENAME: str = "mxbai-embed-06-tabler-icons-full.db"
DATABASE_URL = f"sqlite:///./{DATABASE_DIRECTORY}/{DATABASE_FILENAME}"
logseq_icon_search = FastAPI()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


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


class IconResult(BaseModel):
    name: str
    glyph: str
    similarity_score: float


# Pydantic model for icon keyword search response
class IconSearchResponse(BaseModel):
    result: List[IconResult]


embedding_model = SentenceTransformer(EMBEDDING_MODEL)


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
    db: Session = Depends(get_db)
    ):
    search_query_embedding = semantically_embed(
        embedding_model, f"{query_prompt} {search_string}"
    )
    # all_icons = db.query(Icon).all()
    icons_query = db.query(Icon.name, Icon.glyph, Icon.vector, Icon.tags).all()

    icon_data = []
    for name, glyph, vector, tags in icons_query:
        icon_vector = np.frombuffer(vector, dtype=np.float32)
        similarity_score = cos_sim(search_query_embedding, icon_vector)
        icon_data.append({
            "name": name,
            "glyph": glyph,
            "tags": tags,
            "similarity_score": similarity_score.item(),
        })


    top_results = sorted(icon_data, key=lambda x: x["similarity_score"], reverse=True)[
        :top_k
    ]

    icon_results = [IconResult(**result) for result in top_results]
    return IconSearchResponse(result=icon_results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(logseq_icon_search, host="127.0.0.1", port=8666)
