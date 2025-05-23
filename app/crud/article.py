from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import article as article_schema


def create_article(db: Session, article: article_schema.ArticleCreate):
    db_article = models.article.Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_all_articles(db: Session):
    return db.query(models.article.Article).all()


def get_article_by_id(db: Session, article_id: int):
    article = (
        db.query(models.article.Article)
        .filter(models.article.Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


def update_article(db: Session, article_id: int, data: article_schema.ArticleCreate):
    article = get_article_by_id(db, article_id)
    for key, value in data.model_dump().items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article_id: int):
    article = get_article_by_id(db, article_id)
    db.delete(article)
    db.commit()
    return
