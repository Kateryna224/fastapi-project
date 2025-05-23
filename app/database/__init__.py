from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# 💥 Вот здесь добавляем импорт моделей
from app.models import article, user

# 💥 Создаём таблицы в БД
Base.metadata.create_all(bind=engine)


# Подключение сессии к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
