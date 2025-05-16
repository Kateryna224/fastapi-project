
from fastapi import FastAPI
from app.routes import items

app = FastAPI(title="RPS CRUD", version="1.0.0")

app.include_router(items.router)