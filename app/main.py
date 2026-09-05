from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import projects, tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="IssueFlow API",
    lifespan=lifespan
)


app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {
        "message": "IssueFlow API is running"
    }