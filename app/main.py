from fastapi import FastAPI

from app.api.v1.routes import article, items

app = FastAPI(title="RPS CRUD", version="1.0.0")

app.include_router(items.router)
app.include_router(article.router)
