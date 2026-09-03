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


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.execute(
        select(models.Task)
    ).scalars().all()

    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(
        models.Task,
        task_id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    db_task = db.get(
        models.Task,
        task_id
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            db_task,
            field,
            value
        )

    db.commit()
    db.refresh(db_task)

    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    db_task = db.get(
        models.Task,
        task_id
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(db_task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }