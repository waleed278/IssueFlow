from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post(
    "",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = db.get(
        models.User,
        project.owner_id
    )

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )

    db_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


@router.get(
    "/{project_id}",
    response_model=schemas.ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.get(
        models.Project,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

@router.post(
    "/projects/{project_id}/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    project_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    project = db.get(
        models.Project,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if task.assignee_id is not None:
        assignee = db.get(
            models.User,
            task.assignee_id
        )

        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignee not found"
            )

    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status="todo",
        project_id=project_id,
        assignee_id=task.assignee_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task