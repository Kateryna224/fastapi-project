import os
import sys
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer

from app.api.v1.routes import auth

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import Depends, FastAPI

from app.api.v1.routes import article, items

app = FastAPI(title="RPS CRUD", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app.include_router(items.router)
app.include_router(article.router)
app.include_router(auth.router)


@app.get("/token/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
