from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


def get_project_for_owner(
        db:Session,
        project_id:int,
        user_id: int
)->models.Project:
    project = db.get(
        models.Project,
        project_id
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )

    return project


def create_project(
    db: Session,
    project_data: schemas.ProjectCreate,
    owner: models.User
) -> models.Project:

    project = models.Project(
        name=project_data.name,
        owner_id=owner.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project