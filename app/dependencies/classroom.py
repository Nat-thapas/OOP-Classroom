from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from ..internal.classroom import Classroom
from ..internal.controller import controller
from ..internal.items import BaseItem, SubmissionsMixin
from ..internal.submission import Submission
from ..internal.user import User
from .authentication import get_current_user


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
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User is not classroom owner")


def verify_user_is_student(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
) -> None:
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")
    if user == classroom.owner:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User is classroom owner")
