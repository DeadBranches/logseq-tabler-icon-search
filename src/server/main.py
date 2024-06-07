""" Module description:
    This module implements a semantic search API for the icons table in the
    mxbai-embed-06-tabler-icons-full.db database.
"""

# from contextlib import asynccontextmanager
import os
import sys
import tomllib
from dataclasses import asdict, dataclass, field
from time import time
from typing import Annotated, List, Tuple, Union

import numpy as np
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from icecream import ic
from pydantic import BaseModel
from sentence_transformers import CrossEncoder, SentenceTransformer
from sentence_transformers.util import cos_sim
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

CONFIGURATION_FILENAME = "configuration.toml"
with open(CONFIGURATION_FILENAME, "rb") as f:
    SETTING = tomllib.load(f)

DATASET_PROFILE: str = SETTING.get("dataset")  # "tabler-icons-3.5.0"
DATASET_CONFIG: dict = SETTING["datasets"][SETTING.get("dataset")]
MODEL_CONFIG = SETTING["embedding_model_profile"].get(
    DATASET_CONFIG.get("model_profile")
)


@dataclass
class IconDatabase:
    """
    # Dataset database settings
    Represents the configuration for an icon database.

    ### Arguments:
    - `dataset_profile`: (optional) The name of the dataset profile to use. Defaults to the value in the configuration file.
    - `datasets_directory`: (optional) The directory name relative to main.py containing datasets. Defaults to the value in the configuration file.

    ### Attributes:
    - `dataset_directory`: The sub-directory within datasets_directory containing the specific dataset.
    - `database_filename`: The filename of the database within the dataset_directory.
    - `table_name`: The name of the table within the database to interact with.
    - `database_file`: The full file path to the database file.
    - `database_url`: The URL used to connect to the database.
    """

    dataset_profile: str = SETTING.get("dataset")  # Eit
    datasets_directory: str = SETTING["locations"]["datasets_directory"]
    dataset_directory: str = field(init=False)
    database_filename: str = field(init=False)
    table_name: str = field(init=False)
    database_file: str = field(init=False)
    database_url: str = field(init=False)

    def __post_init__(self):
        profile_data = SETTING["datasets"][self.dataset_profile]
        self.dataset_directory = profile_data["dataset_directory"]
        self.database_filename = profile_data["database_filename"]
        self.table_name = profile_data["table_name"]
        self.database_file = os.path.join(
            sys.path[0],
            self.datasets_directory,
            self.dataset_directory,
            self.database_filename,
        )
        self.database_url = f"sqlite:///./{self.database_file}"


@dataclass
class EmbeddingModel:
    """
    # Embedding model
    Runtime information for using a model with a dataset
    """

    profile_name: str = DATASET_CONFIG["model_profile"]
    model_string: str = field(init=False)
    query_prompt: str = field(init=False)
    encoding_parameters: dict = field(init=False)

    def __post_init__(self):
        self.model_string = MODEL_CONFIG["model_string"]
        self.query_prompt = MODEL_CONFIG["query_prompt"]
        self.encoding_parameters = (
            MODEL_CONFIG.get("encoding_parameters")
            if MODEL_CONFIG.get("encoding_parameters")
            else {}
        )


Base = declarative_base()


class Icon(Base):
    """SQLAlchemy database model to hold table rows."""

    __tablename__ = DATASET_CONFIG["table_name"]
    name = Column(String, primary_key=True)
    tags = Column(String)
    category = Column(String)
    glyph = Column(String)
    vector = Column(String)  # TODO: Check if this is accurate. Should be list?


class IconResult(BaseModel):
    """Pydantic schema for the icon data model to represent a single icon results"""

    name: str
    glyph: str
    keywords: str | None = None
    similarity_score: float | None = None


class IconSearchRequest(BaseModel):
    """Pydantic schema for the icon search request."""

    search_string: str
    negative_search_string: str = None
    top_k: int = 5
    query_prompt: str = "Represent this sentence for searching relevant passages:"


class IconSearchResponse(BaseModel):
    """Pydantic schema for the icon search response."""

    result: List[IconResult]
    debug_info: dict | None = None


ICON_DATABASE_CONFIG = IconDatabase()
EMBEDDING_MODEL_CONFIG = EmbeddingModel()


engine = create_engine(ICON_DATABASE_CONFIG.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
DATABASE_CONTENT = db.query(Icon).all()
db.close()


EMBEDDING_MODEL = SentenceTransformer(EMBEDDING_MODEL_CONFIG.model_string)
rerank_model = CrossEncoder("mixedbread-ai/mxbai-rerank-base-v1")

app = FastAPI()

origins = SETTING["CORS"].get("origins")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def semantically_embed(model, text: str, **kwargs) -> List:
    """Generate a vector embedded with the semantic meaning of the text."""
    text_embedding = model.encode(text, **kwargs)
    return text_embedding


@app.get(
    "/icon-search/{search_string}",
    response_model_exclude_unset=True,
    response_model=IconSearchResponse,
)
async def icon_search(
    search_string: str,
    negative_search: Annotated[List[str] | None, Query()] = None,
    top_k: int = 5,
    query_prompt_template: str | None = None,
    dont_rerank: bool | None = None,
    no_keywords: bool | None = None,
    no_semantic_score: bool | None = None,
    icons=DATABASE_CONTENT,
):
    start_time = time()

    query_prompt_template = (
        # The user may wish to customize the prompt used in addition to the keyword
        query_prompt_template
        if query_prompt_template is not None
        else EMBEDDING_MODEL_CONFIG.query_prompt
    )
    positive_query_prompt = query_prompt_template.replace(
        "xNxREPLACExNx", search_string
    )
    positive_query_embedding = semantically_embed(
        EMBEDDING_MODEL,
        positive_query_prompt,
        **EMBEDDING_MODEL_CONFIG.encoding_parameters,
    )

    query_embedding = positive_query_embedding
    if negative_search is not None:
        negative_query_embeddings = np.array(
            [
                semantically_embed(
                    EMBEDDING_MODEL,
                    query_prompt_template.replace("xNxREPLACExNx", negative_keyword),
                    **EMBEDDING_MODEL_CONFIG.encoding_parameters,
                )
                for negative_keyword in negative_search
            ]
        )
        method = "average"
        if method == "average":
            average_negative_embedding = np.mean(negative_query_embeddings, axis=0)
            query_embedding = positive_query_embedding - average_negative_embedding
        else:

            total_negative_embedding = np.sum(negative_query_embeddings, axis=0)
            # Subtract the sum of negative embeddings from the positive embedding
            query_embedding = positive_query_embedding - total_negative_embedding

    # Method #1
    # icon_data = []
    #     for row in icons:
    #     icon_vector = np.frombuffer(row.vector, dtype=np.float32)
    #     similarity_score = cos_sim(query_embedding, icon_vector)
    #     icon_info = {
    #         "name": row.name,
    #         "glyph": row.glyph,
    #         "keywords": row.tags,
    #         "similarity_score": similarity_score.item(),
    #     }
    #     icon_data.append(icon_info)
    #     top_results = sorted(icon_data, key=lambda x: x["similarity_score"], reverse=True)[
    #     :top_k
    # ]
    # processing_time	620.5425262451172

    # Method 2
    # def create_icon_info(row):
    #     # processing_time	623.6565113067627
    #     icon_vector = np.frombuffer(row.vector, dtype=np.float32)
    #     similarity_score = cos_sim(query_embedding, icon_vector)
    #     return {
    #         "name": row.name,
    #         "glyph": row.glyph,
    #         "keywords": row.tags,
    #         "similarity_score": similarity_score.item(),
    #     }
    # icon_data = list(map(create_icon_info, icons))
    #
    # top_results = sorted(icon_data, key=lambda x: x["similarity_score"], reverse=True)[
    #     :top_k
    # ]

    icon_vectors = np.array(
        [np.frombuffer(row.vector, dtype=np.float32) for row in icons]
    )
    similarity_scores = query_embedding @ icon_vectors.T
    icon_data = [
        {
            "name": row.name,
            "glyph": row.glyph,
            "keywords": row.tags,
            "similarity_score": score.item(),
        }
        for row, score in zip(icons, similarity_scores.flatten())
    ]
    top_results = sorted(icon_data, key=lambda x: x["similarity_score"], reverse=True)[
        :top_k
    ]
    # processing_time 33.99944305419922

    # icon_results = [IconResult(**result) for result in top_results]

    def debug_info(
        rerank=dont_rerank, keywords=no_keywords, semantic_score=no_semantic_score
    ):
        return {
            "processing_time": (time() - start_time) * 1000,
            "dont_rerank": rerank,
            "no_keywords": keywords,
            "no_semantic_score": semantic_score,
            "positive_query_prompt": positive_query_prompt,
            "model": EMBEDDING_MODEL_CONFIG.model_string,
        }

    if (dont_rerank is True) and (no_keywords is None) and (no_semantic_score is None):
        return IconSearchResponse(
            debug_info=debug_info(),
            result=[IconResult(**result) for result in top_results],
        )
    if (dont_rerank is True) and ((no_keywords is True) or (no_semantic_score is True)):
        results = [
            IconResult(
                **{
                    "name": result["name"],
                    "glyph": result["glyph"],
                    **({"keywords": result["keywords"]} if not no_keywords else {}),
                    **(
                        {"similarity_score": result["similarity_score"]}
                        if not no_semantic_score
                        else {}
                    ),
                }
            )
            for result in top_results
        ]
        return IconSearchResponse(
            debug_info=debug_info(),
            result=results,
        )

    rerank_input_query = f"{query_prompt_template} {search_string}"
    rerank_input_documents = [result["keywords"] for result in top_results]

    reranked_results = rerank_model.rank(
        rerank_input_query,
        rerank_input_documents,
        return_documents=True,
    )

    final_results = []
    for item in reranked_results:
        icon = {}
        icon["name"] = top_results[item["corpus_id"]]["name"]
        icon["glyph"] = top_results[item["corpus_id"]]["glyph"]
        icon["keywords"] = top_results[item["corpus_id"]]["keywords"]
        icon["similarity_score"] = item["score"]
        final_results.append(icon)

    return IconSearchResponse(
        result=[IconResult(**result) for result in final_results],
        debug_info=debug_info(),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8667, reload=True)
