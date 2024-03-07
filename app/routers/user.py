from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentication import get_current_user
from ..internal.controller import controller

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", dependencies=[Depends(get_current_user)])
async def get_user(user_id: str):
    user = controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user.to_dict()
