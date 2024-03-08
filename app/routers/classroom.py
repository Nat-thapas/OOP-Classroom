import os
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..config.config import get_settings
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
    AddCommentModel,
    CreateClassroomItemModel,
    CreateClassroomModel,
    CreateClassroomTopicModel,
    GradeSubmissionModel,
    JoinClassroomModel,
    SubmissionModel,
    UpdateClassroomModel,
)

settings = get_settings()

router = APIRouter(
    prefix="/classrooms",
    tags=["Classroom"],
    responses={404: {"description": "Not found"}},
)


@lru_cache
def get_banner_images_cached():
    banner_categories = os.listdir(settings.banner_images_storage_path)
    banner_images: dict[str, list[str]] = {}
    for category in banner_categories:
        category_path = os.path.join(settings.banner_images_storage_path, category)
        for image in os.listdir(category_path):
            if category in banner_images:
                banner_images[category].append(image)
            else:
                banner_images[category] = [image]
    return banner_images


@router.get("")
async def get_classrooms(user: Annotated[User, Depends(get_current_user)]):
    classrooms = controller.get_classrooms_for_user(user)
    return [classroom.to_dict(filter_item_for_user=user) for classroom in classrooms]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_classroom(
    body: CreateClassroomModel, user: Annotated[User, Depends(get_current_user)]
):
    classroom = controller.create_classroom(
        user, body.name, body.section, body.subject, body.room
    )
    return classroom.to_dict(filter_item_for_user=user)


@router.put("")
async def join_classroom(
    body: JoinClassroomModel, user: Annotated[User, Depends(get_current_user)]
):
    classroom = controller.get_classroom_by_code(body.classroom_code)
    if classroom is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid classroom code")
    if user in classroom:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already in classroom")
    classroom.add_student(user)
    return classroom.to_dict(filter_item_for_user=user)


@router.get("/banner-images")
async def get_banner_images():
    return get_banner_images_cached()


@router.get("/{classroom_id}", dependencies=[Depends(verify_user_in_classroom)])
async def get_classroom(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    include_code = user == classroom.owner
    return classroom.to_dict(
        include_code=include_code, include_lists=True, filter_item_for_user=user
    )


@router.patch(
    "/{classroom_id}",
    dependencies=[Depends(get_current_user), Depends(verify_user_is_classroom_owner)],
)
async def update_classroom(
    body: UpdateClassroomModel,
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    classroom.name = body.name
    classroom.section = body.section
    classroom.subject = body.subject
    classroom.room = body.room
    classroom.banner_path = body.banner_path
    return classroom.to_dict()


@router.delete(
    "/{classroom_id}",
    dependencies=[Depends(get_current_user), Depends(verify_user_is_classroom_owner)],
)
async def delete_classroom(
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)]
):
    controller.delete_classroom(classroom)
    return {"message": "Classroom deleted successfully"}


@router.get(
    "/{classroom_id}/topics",
    dependencies=[Depends(get_current_user), Depends(verify_user_in_classroom)],
)
async def get_classroom_topics(
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    return [topic.to_dict() for topic in classroom.topics]


@router.post(
    "/{classroom_id}/topics",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user), Depends(verify_user_is_classroom_owner)],
)
async def create_classroom_topic(
    body: CreateClassroomTopicModel,
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    topic = classroom.create_topic(body.name)
    return topic.to_dict()


@router.get("/{classroom_id}/items", dependencies=[Depends(verify_user_in_classroom)])
async def get_classroom_items(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    return [
        item.to_dict()
        for item in classroom.items
        if item.assigned_to_students is None
        or user in item.assigned_to_students
        or user == classroom.owner
    ]


@router.post(
    "/{classroom_id}/items",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user), Depends(verify_user_is_classroom_owner)],
)
async def create_classroom_item(
    body: CreateClassroomItemModel,
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
):
    item_type = body.type
    if body.topic_id:
        topic = classroom.get_topic_by_id(body.topic_id)
        if topic is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid topic ID")
    else:
        topic = None
    attachments = list(map(controller.get_attachment_by_id, body.attachments_id))
    if None in attachments:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid attachment ID")
    attachments = [attachment for attachment in attachments if attachment]
    if body.assigned_to_students_id:
        assigned_to_students = list(
            map(controller.get_user_by_id, body.assigned_to_students_id)
        )
        if None in assigned_to_students:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid student ID")
        assigned_to_students = [student for student in assigned_to_students if student]
    else:
        assigned_to_students = None
    try:
        if item_type == ClassroomItemType.ANNOUNCEMENT:
            announcement_text = body.announcement_text
            if announcement_text is None:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Announcement text is required"
                )
            announcement = classroom.create_announcement(
                attachments, assigned_to_students, announcement_text
            )
            return announcement.to_dict()

        title = body.title
        if title is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Title is required")
        description = body.description

        if item_type == ClassroomItemType.MATERIAL:
            material = classroom.create_material(
                topic, attachments, assigned_to_students, title, description
            )
            return material.to_dict()

        due_date = body.due_date
        point = body.point

        if item_type == ClassroomItemType.ASSIGNMENT:
            assignment = classroom.create_assignment(
                topic,
                attachments,
                assigned_to_students,
                title,
                description,
                due_date,
                point,
            )
            return assignment.to_dict()

        if item_type == ClassroomItemType.QUESTION:
            question = classroom.create_question(
                topic,
                attachments,
                assigned_to_students,
                title,
                description,
                due_date,
                point,
            )
            return question.to_dict()

        choices = body.choices
        if choices is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "At least one choice is required"
            )

        if item_type == ClassroomItemType.MULTIPLE_CHOICE_QUESTION:
            multiple_choice_question = classroom.create_multiple_choice_question(
                topic,
                attachments,
                assigned_to_students,
                title,
                description,
                due_date,
                point,
                choices,
            )
            return multiple_choice_question.to_dict()

        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid item type")

    except ValueError as exp:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data") from exp


@router.get(
    "/{classroom_id}/items/{item_id}", dependencies=[Depends(verify_user_in_classroom)]
)
async def get_classroom_item(
    user: Annotated[User, Depends(get_current_user)],
    classroom: Annotated[Classroom, Depends(get_classroom_from_path)],
    item: Annotated[BaseItem, Depends(get_item_from_path)],
):
    if (
        item.assigned_to_students is None
        or user in item.assigned_to_students
        or user == classroom.owner
    ):
        return item.to_dict()
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")


@router.post(
    "/{classroom_id}/items/{item_id}/comments",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_user_in_classroom)],
)
async def add_comment_to_classroom_item(
    body: AddCommentModel,
    user: Annotated[User, Depends(get_current_user)],
    item: Annotated[BaseItem, Depends(get_item_from_path)],
):
    item.create_comment(user, body.comment)
    return item.to_dict()


@router.get(
    "/{classroom_id}/items/{item_id}/submissions",
    dependencies=[Depends(get_current_user), Depends(verify_user_is_classroom_owner)],
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
    status_code=status.HTTP_201_CREATED,
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


@router.post(
    "/{classroom_id}/items/{item_id}/submissions/@me/comments",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_user_is_student)],
)
async def add_comment_to_my_submission(
    body: AddCommentModel,
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
    submission.create_comment(user, body.comment)
    return submission.to_dict()


@router.put(
    "/{classroom_id}/items/{item_id}/submissions/{submission_id}",
    dependencies=[Depends(get_current_user), Depends(verify_user_is_classroom_owner)],
)
async def grade_classroom_item_submission(
    body: GradeSubmissionModel,
    submission: Annotated[Submission, Depends(get_submission_from_path)],
):
    if submission is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Submission not found")
    submission.point = body.point
    return submission.to_dict()


@router.post(
    "/{classroom_id}/items/{item_id}/submissions/{submission_id}/comments",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_user_is_classroom_owner)],
)
async def add_comment_to_submission(
    body: AddCommentModel,
    user: Annotated[User, Depends(get_current_user)],
    submission: Annotated[Submission, Depends(get_submission_from_path)],
):
    if submission is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Submission not found")
    submission.create_comment(user, body.comment)
    return submission.to_dict()
