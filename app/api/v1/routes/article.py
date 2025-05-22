from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Path, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/articles", tags=["articles"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=schemas.Article)
def create_article(article: Annotated[schemas.ArticleCreate, Body()], db: DB):
    db_article = models.Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.get("/", response_model=List[schemas.Article])
def read_articles(
    db: DB,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    articles = db.query(models.Article).offset(skip).limit(limit).all()
    return articles


@router.get("/{article_id}", response_model=schemas.Article)
def read_article(
    article_id: Annotated[int, Path(title="The ID of the article to get", ge=1)], db: DB
):
    pass


@router.put("/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: Annotated[int, Path(title="The ID of the article to update", ge=1)],
    updated_article: Annotated[schemas.ArticleCreate, Body()],
    db: DB,
):
    pass


@router.delete("/{article_id}")
def delete_article(
    article_id: Annotated[int, Path(title="The ID of the article to delete", ge=1)],
    db: DB,
):
    pass
