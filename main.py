from contextlib import asynccontextmanager
from typing import Literal

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="IssueFlow API",
    lifespan=lifespan
)


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    priority: Literal[
        "low",
        "medium",
        "high"
    ]

class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    priority: Literal[
        "low",
        "medium",
        "high"
    ] | None = None

    status: Literal[
        "todo",
        "in_progress",
        "done"
    ] | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Literal[
        "low",
        "medium",
        "high"
    ]
    status: Literal[
        "todo",
        "in_progress",
        "done"
    ]

    model_config = {
        "from_attributes": True
    }


@app.get("/")
def home():
    return {
        "message": "IssueFlow API is running"
    }

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status="todo"
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task
