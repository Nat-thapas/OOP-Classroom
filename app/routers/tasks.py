from typing import Annotated

from fastapi import APIRouter, Depends

from ..constants.enums import TaskType
from ..dependencies.authentication import get_current_user
from ..internal.controller import controller
from ..internal.user import User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)


@router.get("/@me")
async def get_tasks(task_type: TaskType, user: Annotated[User, Depends(get_current_user)]):
    tasks = controller.get_tasks_for_user(user, task_type)
    return [task.to_dict() for task in tasks]
