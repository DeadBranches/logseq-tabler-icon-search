from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Tuple, Dict
import random

TABLE_NAME: str = "icons"
DATABASE_DIRECTORY: str = "databases"
DATABASE_FILENAME: str = "mxbai-embed-06-tabler-icons-full.db"
DATABASE_URL = f"sqlite:///./{DATABASE_DIRECTORY}/{DATABASE_FILENAME}"
app = FastAPI()
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


def calculate_similarity(vector1, vector2):
    # generate a random float between 0 and 1
    random_float = random.random()
    return random_float


@app.get("/icon-search/{search_string}", response_model=IconSearchResponse)
async def icon_search(
    search_string: str,
    top_k: int = 5,
    query_prompt: str = None,
    db: Session = Depends(get_db),
):
    icons = db.query(Icon).all()
    search_results = [
        {
            "name": icon.name,
            "glyph": icon.glyph,
            "similarity_score": calculate_similarity(icon.vector, search_string),
        }
        for icon in icons
    ]
    top_results = sorted(
        search_results, key=lambda x: x["similarity_score"], reverse=True
    )[:top_k]

    if search_results is None:
        raise HTTPException(status_code=404, detail="Icon not found")

    icon_results = [IconResult(**result) for result in top_results]
    return IconSearchResponse(result=icon_results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
