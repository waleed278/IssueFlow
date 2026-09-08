from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from app.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(
    plain_password: str
) -> str:
    return password_hasher.hash(
        plain_password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hasher.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    user_id: int
) -> str:
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

def decode_access_token(
        token:str
)->int:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm]
    )
    subject = payload.get("sub")
    if subject is None:
        raise InvalidTokenError(
            "Missing subject"
        )

    return int(subject)