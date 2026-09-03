from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI()


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

class TaskListResponse(BaseModel):
    tasks : list[TaskResponse]

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Understand FastAPI fundamentals",
        "priority": "high",
        "status": "todo"
    },
    {
        "id": 2,
        "title": "Build IssueFlow",
        "description": "Build our first backend project",
        "priority": "medium",
        "status": "in_progress"
    }
]


@app.get("/")
def home():
    return {
        "message": "IssueFlow API is running"
    }


@app.get("/tasks",response_model=TaskListResponse)
def get_tasks():
    return {
        "tasks": tasks
    }


@app.get("/tasks/{task_id}",response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):
    if tasks:
        new_id = tasks[-1]["id"] + 1
    else:
        new_id = 1

    task_data = task.model_dump()

    new_task = {
        "id": new_id,
        **task_data,
        "status": "todo"
    }

    tasks.append(new_task)

    return new_task


@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate
):
    for task in tasks:
        if task["id"] == task_id:
            update_data = task_update.model_dump(
                exclude_unset=True
            )

            for field, value in update_data.items():
                task[field] = value

            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )