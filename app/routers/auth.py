from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

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
    existing_user = db.scalar(
        select(models.User).where(models.User.email==user.email)
    )

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already eixts")

    hashed_password = hash_password(user.password)

    db_user = models.User(
        name = user.name,
        email = user.email,
        password_hash = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login",response_model=schemas.TokenResponse)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db:Session = Depends(get_db)
):
    db_user = db.scalar(select(models.User).where(models.User.email==form_data.username))

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")

    if not verify_password(form_data.password,db_user.password_hash):
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
         )
    access_token = create_access_token(
        db_user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }