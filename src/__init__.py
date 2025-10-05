from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.books.books import bookRouter
from db.main import init_db

version = "v1"


@asynccontextmanager
async def lifeSpan(app:FastAPI):
    print("Starting the server")
    await init_db()
    yield
    print("Stopping the server")

app = FastAPI(
    title="Book API",
    version=version,
    lifespan=lifeSpan
)

app.include_router(router=bookRouter, prefix=f"/api/{version}/books", tags=["books"])
