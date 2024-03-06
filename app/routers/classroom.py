from fastapi import APIRouter, Depends, HTTPException, status

from ..constants.enums import ClassroomItemType
from ..dependencies.dependencies import get_current_user
from ..internal.controller import controller
from ..internal.user import User
from ..models.classroom import (
    CreateClassroomItemModel,
    CreateClassroomModel,
    JoinClassroomModel,
)

router = APIRouter(
    prefix="/classroom",
    tags=["Classroom"],
    responses={404: {"description": "Not found"}},
)


@router.get("/classrooms")
async def get_classrooms(user: User = Depends(get_current_user)):
    classrooms = controller.get_classrooms_for_user(user)
    return [classroom.to_dict() for classroom in classrooms]


@router.post("/classrooms")
async def create_classroom(
    body: CreateClassroomModel, user: User = Depends(get_current_user)
):
    classroom = controller.create_classroom(
        user, body.name, body.section, body.subject, body.room
    )
    return classroom.to_dict()


@router.put("/classrooms")
async def join_classroom(
    body: JoinClassroomModel, user: User = Depends(get_current_user)
):
    classroom = controller.get_classroom_by_code(body.classroom_code)
    if classroom is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid classroom code")
    if user in classroom:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already in classroom")
    classroom.add_student(user)
    return classroom.to_dict()


@router.get("/classrooms/{classroom_id}")
async def get_classroom(classroom_id: str, user: User = Depends(get_current_user)):
    classroom = controller.get_classroom_by_id(classroom_id)
    if classroom is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")
    include_code = user == classroom.owner
    return classroom.to_dict(include_code=include_code, include_lists=True)


@router.get("classrooms/{classroom_id}/items")
async def get_classroom_items(
    classroom_id: str, user: User = Depends(get_current_user)
):
    classroom = controller.get_classroom_by_id(classroom_id)
    if classroom is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")
    return [item.to_dict() for item in classroom.items]


@router.post("/classrooms/{classroom_id}/items")
async def create_classroom_item(
    classroom_id: str,
    body: CreateClassroomItemModel,
    user: User = Depends(get_current_user),
):
    classroom = controller.get_classroom_by_id(classroom_id)
    if classroom is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")
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


@router.get("/classrooms/{classroom_id}/items/{item_id}")
async def get_classroom_item(
    classroom_id: str, item_id: str, user: User = Depends(get_current_user)
):
    classroom = controller.get_classroom_by_id(classroom_id)
    if classroom is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    if user not in classroom:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not in classroom")
    item = classroom.get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return item.to_dict()
