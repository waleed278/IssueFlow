from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from app import schemas
from app import models
from app.database import get_db
from app.dependencies import get_current_user

from app.services import membership_service
router = APIRouter(
    prefix="/projects",
    tags=["Project Memberships"],
)


@router.post("/{project_id}/members",
             response_model=schemas.ProjectMembershipResponse,
             status_code=status.HTTP_201_CREATED)

def add_member(
    project_id:int,
    member_data: schemas.ProjectMemberAdd,
    db:Session =  Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    ),

):

    return membership_service.add_project_member(
        db=db,
        project_id=project_id,
        target_user_id=member_data.user_id,
        current_user_id=current_user.id,
    )

@router.get("/{project_id}/members",response_model=list[schemas.ProjectMembershipResponse])

def list_members():
    pass