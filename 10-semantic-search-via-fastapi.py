from typing import List, Tuple, Dict, Any, Annotated
import random

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from icecream import ic
from pydantic import BaseModel
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, Any
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session, declarative_base

EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"

TABLE_NAME: str = "icons"
DATABASE_DIRECTORY: str = "databases"
DATABASE_FILENAME: str = "mxbai-embed-06-tabler-icons-full.db"
DATABASE_URL = f"sqlite:///./{DATABASE_DIRECTORY}/{DATABASE_FILENAME}"


# Define embedding_model as a global variable
embedding_model = Any

@asynccontextmanager
async def lifespan(app: FastAPI):
    global embedding_model 
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    yield

app = FastAPI(lifespan=lifespan)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

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
    keywords: str
    similarity_score: float


# Pydantic model for icon keyword search response
class IconSearchResponse(BaseModel):
    result: List[IconResult]


def semantically_embed(model, text: str) -> List:
    """Generate a vector embedded with the semantic meaning of the text."""
    text_embedding = model.encode(text)
    return text_embedding


@app.get(
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
