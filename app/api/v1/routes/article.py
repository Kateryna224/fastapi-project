from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import article as crud_article
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas import article as article_schema

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/", response_model=article_schema.Article)
def create_article(
    article: article_schema.ArticleCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    return crud_article.create_article(db, article)


@router.get("/", response_model=list[article_schema.Article])
def get_all_articles(
    db: Session = Depends(get_db), user: str = Depends(get_current_user)
):
    return crud_article.get_all_articles(db)


@router.get("/{article_id}", response_model=article_schema.Article)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    return crud_article.get_article_by_id(db, article_id)


@router.put("/{article_id}", response_model=article_schema.Article)
def update_article(
    article_id: int,
    updated_data: article_schema.ArticleCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    return crud_article.update_article(db, article_id, updated_data)


@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    return crud_article.delete_article(db, article_id)
