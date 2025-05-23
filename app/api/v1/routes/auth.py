import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import user as user_schema

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "секретный_ключ_катюши"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (
        expires_delta or datetime.timedelta(minutes=30)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.user.User)
        .filter(models.user.User.username == user.username)
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    new_user = models.user.User(
        username=user.username, password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "Регистрация успешна"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = form_data.username
    password = form_data.password
    db_user = (
        db.query(models.user.User).filter(models.user.User.username == user).first()
    )
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Неверные данные")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
