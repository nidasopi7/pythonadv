from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from routers import categories, recipes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Online Recipe Book API",
    description="Manage recipes and categories",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(categories.router)
app.include_router(recipes.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Online Recipe Book API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}