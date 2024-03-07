from datetime import datetime, timedelta
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..config.config import get_settings
from ..internal.classroom import Classroom
from ..internal.controller import controller
from ..internal.items import BaseItem, SubmissionsMixin
from ..internal.user import User
from ..internal.submission import Submission

settings = get_settings()

password_hasher = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(hashed_password: str, plain_password: str) -> bool:
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


def authenticate_user(username_or_email: str, password: str) -> User | None:
    user = controller.get_user_by_email(
        username_or_email
    ) or controller.get_user_by_username(username_or_email)
    if user is None:
        return None
    if not verify_password(user.hashed_password, password):
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


def get_classroom_from_path(classroom_id: Annotated[str, Path()]) -> Classroom:
    classroom = controller.get_classroom_by_id(classroom_id)
    if classroom is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    return classroom


def get_item_from_path(
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
    item_id: Annotated[str, Path()],
) -> BaseItem:
    item = classroom.get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return item

def get_submission_from_path(
    item: Annotated[BaseItem, Depends(get_item_from_path)],
    submission_id: Annotated[str, Path()],
) -> Submission:
    if not isinstance(item, SubmissionsMixin):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Item type does not support submission"
        )
    submission = item.get_submission_by_id(submission_id)
    if submission is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Submission not found")
    return submission

def verify_user_in_classroom(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
) -> None:
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")

def verify_user_is_classroom_owner(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
) -> None:
    if user != classroom.owner:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User is not classroom owner"
        )

def verify_user_is_student(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
) -> None:
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")
    if user == classroom.owner:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "User is classroom owner"
        )
