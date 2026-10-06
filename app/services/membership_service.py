from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.services.project_service import (
    require_project_owner, require_project_member
)

def add_project_member(
        db:Session,
        project_id: int,
        target_user_id:int,
        current_user_id:int,
)-> models.ProjectMembership:
    require_project_owner(
        db=db,
        project_id=project_id,
        user_id=current_user_id,
    )
    target_user = db.get(models.User,target_user_id)

    if target_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    existing_membership =  db.scalar(
        select(models.ProjectMembership).where(
            models.ProjectMembership.project_id==project_id,
            models.ProjectMembership.user_id== target_user_id,
        )
    )
    if existing_membership is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a project member"

        )
    membership = models.ProjectMembership(
        project_id=project_id,
        user_id=target_user_id,
        role="member",
    )

    db.add(membership)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a project member",
        )

    db.refresh(membership)

    return membership

def list_project_members(
        db:Session,
        project_id:int,
        current_user_id: int,
):
    require_project_member(
        db=db,
        project_id=project_id,
        user_id=current_user_id
    )

    return db.scalar(
        select(models.ProjectMembership)
        .where(models.ProjectMembership.project_id==project_id)
        .order_by(
            models.ProjectMembership.id.asc()
        )
    ).all()
