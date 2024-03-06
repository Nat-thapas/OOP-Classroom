from datetime import datetime, timedelta
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..config.config import get_settings
from ..internal.user import User
from ..internal.controller import controller

settings = get_settings()

password_hasher = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        password_hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    return True


def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def authenticate_user(email: str, password: str) -> User | None:
    user = controller.get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        user_id_payload = payload.get("id")
        if not isinstance(user_id_payload, str):
            raise credentials_exception
        user_id: str = user_id_payload
    except JWTError as exc:
        raise credentials_exception from exc

    user = controller.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
