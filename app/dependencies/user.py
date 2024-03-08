from typing import Annotated

from fastapi import HTTPException, Path, status

from ..internal.controller import controller
from ..internal.user import User


def get_user_from_path(user_id: Annotated[str, Path()]) -> User:
    user = controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user
