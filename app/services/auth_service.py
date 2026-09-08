from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from app import models, schemas
from app.security import(
    create_access_token,
    hash_password,
    verify_password
)

def register_user(db:Session,
                  user_data:schemas.UserRegister)->models.User:

    existing_user = db.scalar(select(models.User).where(models.User.email==user_data.email))

    if existing_user is not None:
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = models.User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        )
    )

    db.add(user)

    try:
         db.commit()
    except IntegrityError:
         db.rollback()
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    db.refresh(user)
    return user


def authenticate_user(
          db:Session,
          email:str,
          password:str
):
    user = db.scalar(select(models.User).where(models.User.email==email))

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(
         password,
         user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    return create_access_token(user.id)