from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal

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
    priority: Literal["low", "medium", "high"]


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

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    if tasks:
        new_id =  tasks[-1]["id"] + 1
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

@app.get("/")
def home():
    return {
        "message": "IssueFlow API is running"
    }


@app.get("/tasks")
def get_tasks():
    return {
        "tasks": tasks
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
