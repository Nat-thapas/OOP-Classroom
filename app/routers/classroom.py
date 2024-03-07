from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..constants.enums import ClassroomItemType
from ..dependencies.authentication import get_current_user
from ..dependencies.classroom import (
    get_classroom_from_path,
    get_item_from_path,
    get_submission_from_path,
    verify_user_in_classroom,
    verify_user_is_classroom_owner,
    verify_user_is_student,
)
from ..internal.classroom import Classroom
from ..internal.controller import controller
from ..internal.items import BaseItem, SubmissionsMixin
from ..internal.submission import Submission
from ..internal.user import User
from ..models.classroom import (
    CreateClassroomItemModel,
    CreateClassroomModel,
    GradeSubmissionModel,
    JoinClassroomModel,
    SubmissionModel,
)

router = APIRouter(
    prefix="/classrooms",
    tags=["Classroom"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_classrooms(user: Annotated[User, Depends(get_current_user)]):
    classrooms = controller.get_classrooms_for_user(user)
    return [classroom.to_dict() for classroom in classrooms]


@router.post("/", status_code=201)
async def create_classroom(
    body: CreateClassroomModel, user: Annotated[User, Depends(get_current_user)]
):
    classroom = controller.create_classroom(
        user, body.name, body.section, body.subject, body.room
    )
    return classroom.to_dict()


@router.put("/")
async def join_classroom(
    body: JoinClassroomModel, user: Annotated[User, Depends(get_current_user)]
):
    classroom = controller.get_classroom_by_code(body.classroom_code)
    if classroom is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid classroom code")
    if user in classroom:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already in classroom")
    classroom.add_student(user)
    return classroom.to_dict()


@router.get("/{classroom_id}", dependencies=[Depends(verify_user_in_classroom)])
async def get_classroom(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    include_code = user == classroom.owner
    return classroom.to_dict(include_code=include_code, include_lists=True)


@router.get("/{classroom_id}/items", dependencies=[Depends(verify_user_in_classroom)])
async def get_classroom_items(
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    return [item.to_dict() for item in classroom.items]


@router.post(
    "/{classroom_id}/items",
    status_code=201,
    dependencies=[Depends(verify_user_is_classroom_owner)],
)
async def create_classroom_item(
    body: CreateClassroomItemModel,
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    item_type = body.type
    topic = classroom.get_topic_by_id(body.topic_id) if body.topic_id else None
    attachments = list(map(controller.get_attachment_by_id, body.attachments_id))
    attachments = [attachment for attachment in attachments if attachment]
    assigned_to_students = list(
        map(controller.get_user_by_id, body.assigned_to_students_id)
    )
    assigned_to_students = [student for student in assigned_to_students if student]
    try:
        if item_type == ClassroomItemType.ANNOUNCEMENT:
            announcement_text = body.announcement_text
            if announcement_text is None:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Announcement text is required"
                )
            return classroom.create_announcement(
                attachments, assigned_to_students, announcement_text
            )

        title = body.title
        if title is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Title is required")
        description = body.description

        if item_type == ClassroomItemType.MATERIAL:
            return classroom.create_material(
                topic, attachments, assigned_to_students, title, description
            )

        due_date = body.due_date
        point = body.point

        if item_type == ClassroomItemType.ASSIGNMENT:
            return classroom.create_assignment(
                topic,
                attachments,
                assigned_to_students,
                title,
                description,
                due_date,
                point,
            )

        if item_type == ClassroomItemType.QUESTION:
            return classroom.create_question(
                topic,
                attachments,
                assigned_to_students,
                title,
                description,
                due_date,
                point,
            )

        choices = body.choices
        if choices is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "At least one choice is required"
            )

        if item_type == ClassroomItemType.MULTIPLE_CHOICE_QUESTION:
            return classroom.create_multiple_choice_question(
                topic,
                attachments,
                assigned_to_students,
                title,
                description,
                due_date,
                point,
                choices,
            )

        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid item type")

    except ValueError as exp:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data") from exp


@router.get(
    "/{classroom_id}/items/{item_id}", dependencies=[Depends(verify_user_in_classroom)]
)
async def get_classroom_item(
    item: Annotated[BaseItem, Depends(get_item_from_path)],
):
    return item.to_dict()


@router.get(
    "/{classroom_id}/items/{item_id}/submissions",
    dependencies=[Depends(verify_user_is_classroom_owner)],
)
async def get_classroom_item_submissions(
    item: Annotated[BaseItem, Depends(get_item_from_path)],
):
    if not isinstance(item, SubmissionsMixin):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Item type does not support submission"
        )
    return [submission.to_dict() for submission in item.submissions]


@router.get(
    "/{classroom_id}/items/{item_id}/submissions/@me",
    dependencies=[Depends(verify_user_is_student)],
)
async def get_classroom_item_submission(
    user: Annotated[User, Depends(get_current_user)],
    item: Annotated[BaseItem, Depends(get_item_from_path)],
):
    if not isinstance(item, SubmissionsMixin):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Item type does not support submission"
        )
    submission = item.get_submission_by_owner(user)
    if not submission:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Submission not found")
    return submission.to_dict()


@router.post(
    "/{classroom_id}/items/{item_id}/submissions/@me",
    status_code=201,
    dependencies=[Depends(verify_user_is_student)],
)
async def add_classroom_item_submission(
    body: SubmissionModel,
    user: Annotated[User, Depends(get_current_user)],
    item: Annotated[BaseItem, Depends(get_item_from_path)],
):
    if not isinstance(item, SubmissionsMixin):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Item type does not support submission"
        )
    attachments = list(map(controller.get_attachment_by_id, body.attachments_id))
    attachments = [attachment for attachment in attachments if attachment]
    return item.create_submission(user, attachments).to_dict()


@router.put(
    "/{classroom_id}/items/{item_id}/submissions/{submission_id}",
    dependencies=[Depends(verify_user_is_classroom_owner)],
)
async def grade_classroom_item_submission(
    body: GradeSubmissionModel,
    submission: Annotated[Submission, Depends(get_submission_from_path)],
):
    if submission is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Submission not found")
    submission.point = body.point
    return submission.to_dict()
