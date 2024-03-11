from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..dependencies.authentication import (
    get_current_user,
    get_password_hash,
    verify_password,
)
from ..dependencies.user import get_user_from_path
from ..internal.controller import controller
from ..internal.user import User
from ..models.user import UpdateUserModel

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/@me")
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user.to_dict()


@router.patch("/@me")
async def update_me(
    body: UpdateUserModel, user: Annotated[User, Depends(get_current_user)]
):
    if (
        controller.get_user_by_email(body.email) is not None
        and controller.get_user_by_email(body.email) != user
    ):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already in use")
    if (
        controller.get_user_by_username(body.username) is not None
        and controller.get_user_by_username(body.username) != user
    ):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already in use")
    if not verify_password(user.hashed_password, body.old_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Old password is incorrect")
    user.email = body.email
    user.username = body.username
    if body.new_password:
        user.hashed_password = get_password_hash(body.new_password)
    return user.to_dict()


@router.get("/{user_id}", dependencies=[Depends(get_current_user)])
async def get_user(user: Annotated[User, Depends(get_user_from_path)]):
    return user.to_dict()


@router.get("/{user_id}/avatar")
async def get_user_avatar_info(user: Annotated[User, Depends(get_user_from_path)]):
    return user.avatar.to_dict()


@router.get("/{user_id}/avatar/data")
async def get_user_avatar_data(user: Annotated[User, Depends(get_user_from_path)]):
    return Response(user.avatar.data.getvalue(), media_type=user.avatar.content_type)
