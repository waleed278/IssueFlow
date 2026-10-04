from typing import Literal

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: str = Field(
        min_length=5,
        max_length=255
    )
    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }

class TokenResponse(BaseModel):
    access_token : str
    token_type: str


class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=150
    )

    


class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = {
        "from_attributes": True
    }

class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150
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

    assignee_id: int | None = None


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

    assignee_id: int | None = None


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
    project_id: int
    assignee_id: int | None

    model_config = {
        "from_attributes": True
    }

class TaskPageResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    limit: int
    offset: int