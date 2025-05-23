from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import article as article_schema

router = APIRouter(prefix="/articles", tags=["articles"])


# POST — создание статьи
@router.post("/", response_model=article_schema.Article)
def create_article(
    article: article_schema.ArticleCreate, db: Session = Depends(get_db)
):
    db_article = models.article.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


# GET по ID
@router.get("/{article_id}", response_model=article_schema.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(models.article.Article)
        .filter(models.article.Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


# PUT — обновление статьи
@router.put("/{article_id}", response_model=article_schema.Article)
def update_article(
    article_id: int,
    updated_data: article_schema.ArticleCreate,
    db: Session = Depends(get_db),
):
    article = (
        db.query(models.article.Article)
        .filter(models.article.Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    for key, value in updated_data.dict().items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article


# DELETE — удаление статьи
@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(models.article.Article)
        .filter(models.article.Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    db.delete(article)
    db.commit()
    return
