from fastapi import APIRouter, Depends, HTTPException, status

from ..internal.user import User
from ..internal.controller import controller
from ..dependencies.dependencies import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/users/{user_id}")
async def get_user(user_id: str, _: User = Depends(get_current_user)):
    user = controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user.to_dict()
