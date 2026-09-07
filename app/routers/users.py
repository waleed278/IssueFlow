from fastapi import APIRouter, Depends
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me",response_model=schemas.UserResponse)
def get_me(current_user:models.User = Depends(get_current_user)):
    return current_user