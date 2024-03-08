from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentication import get_current_user, verify_password, get_password_hash
from ..models.user import UpdateUserModel
from ..internal.controller import controller
from ..internal.user import User

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/@me")
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user.to_dict()


@router.patch("/@me")
async def update_me(body: UpdateUserModel, user: Annotated[User, Depends(get_current_user)]):
    if controller.get_user_by_email(body.email) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already in use")
    if controller.get_user_by_username(body.username) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already in use")
    if not verify_password(user.hashed_password, body.old_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Old password is incorrect")
    user.email = body.email
    user.username = body.username
    if body.new_password:
        user.hashed_password = get_password_hash(body.new_password)
    return user.to_dict()


@router.get("/{user_id}", dependencies=[Depends(get_current_user)])
async def get_user(user_id: str):
    user = controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user.to_dict()
