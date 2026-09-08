from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from app.services import auth_service

from app import models , schemas
from app.database import get_db
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",
             response_model=schemas.UserResponse,
             status_code=status.HTTP_201_CREATED)

def register(user:schemas.UserRegister,
             db: Session = Depends(get_db)):

    return auth_service.register_user(
        db=db,
        user_data=user
        )
    


@router.post("/login",response_model=schemas.TokenResponse)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db:Session = Depends(get_db)
):
    access_token = auth_service.authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }