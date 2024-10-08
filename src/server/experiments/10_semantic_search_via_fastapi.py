""" Module description:
    This module implements a semantic search API for the icons table in the
    sqlite3 database.
"""

# from contextlib import asynccontextmanager
from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# region Configuration
EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"
TABLE_NAME: str = "icons"
DATABASE_DIRECTORY: str = "../"
DATABASE_FILENAME: str = "tabler-icons.sqlite3"
DATABASE_URL = f"sqlite:///./{DATABASE_DIRECTORY}/{DATABASE_FILENAME}"
# endregion


# region database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Icon(Base):
    """SQLAlchemy database model to hold table rows."""

    __tablename__ = TABLE_NAME
    name = Column(String, primary_key=True)
    tags = Column(String)
    category = Column(String)
    glyph = Column(String)
    vector = Column(String)  # TODO: Check if this is accurate. Should be list?


class IconResult(BaseModel):
    """Pydantic schema for the icon data model to represent a single icon result."""

    name: str
    glyph: str
    keywords: str
    similarity_score: float


class IconSearchRequest(BaseModel):
    """Pydantic schema for the icon search request."""

    search_string: str
    top_k: int = 5
    query_prompt: str = "Represent this sentence for searching relevant passages:"


class IconSearchResponse(BaseModel):
    """Pydantic schema for the icon search response."""

    result: List[IconResult]


db = SessionLocal()
tabler_icons = db.query(Icon).all()
db.close()
# endregion


embedding_model = SentenceTransformer(EMBEDDING_MODEL)

app = FastAPI()


def semantically_embed(model, text: str) -> List:
    """Generate a vector embedded with the semantic meaning of the text."""
    text_embedding = model.encode(text)
    return text_embedding


@app.get("/icon-search/{search_string}", response_model=IconSearchResponse)
async def icon_search(
    search_string: str,
    top_k: int = 5,
    query_prompt: str = "Represent this sentence for searching relevant passages:",
    icons=tabler_icons,
):
    """Perform a semantic search for icons based on the search string."""
    search_query_embedding = semantically_embed(
        embedding_model, f"{query_prompt} {search_string}"
    )

    icon_data = []
    for row in icons:
        icon_vector = np.frombuffer(row.vector, dtype=np.float32)
        similarity_score = cos_sim(search_query_embedding, icon_vector)
        icon_info = {
            "name": row.name,
            "glyph": row.glyph,
            "keywords": row.tags,
            "similarity_score": similarity_score.item(),
        }
        icon_data.append(icon_info)

    top_results = sorted(icon_data, key=lambda x: x["similarity_score"], reverse=True)[
        :top_k
    ]

    icon_results = [IconResult(**result) for result in top_results]
    return IconSearchResponse(result=icon_results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8666)
