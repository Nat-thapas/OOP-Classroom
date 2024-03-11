from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, validator

from ..config.config import get_settings
from ..constants.enums import ClassroomItemType
from ..internal.classroom import get_valid_banner_images

settings = get_settings()


class CreateClassroomModel(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=48)]
    section: Annotated[str, Field(min_length=1, max_length=16)] | None
    subject: Annotated[str, Field(min_length=1, max_length=32)] | None
    room: Annotated[str, Field(min_length=1, max_length=16)] | None

class UpdateClassroomModel(CreateClassroomModel):
    banner_path: str
    theme_color: str

    @validator("banner_path")
    @classmethod
    def validate_banner_path(cls, value: str) -> str:
        if value not in get_valid_banner_images():
            raise ValueError("Invalid banner path")
        return value

    @validator("theme_color")
    @classmethod
    def validate_theme_color(cls, value: str) -> str:
        if value not in settings.theme_colors:
            raise ValueError("Invalid theme color")
        return value

class JoinClassroomModel(BaseModel):
    classroom_code: Annotated[
        str,
        Field(
            min_length=settings.classroom_code_length,
            max_length=settings.classroom_code_length,
        ),
    ]


class CreateClassroomTopicModel(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=64)]


class CreateClassroomItemModel(BaseModel):
    type: ClassroomItemType
    topic_id: str | None
    attachments_id: Annotated[list[str], MaxLen(8)]
    assigned_to_students_id: list[str] | None
    title: Annotated[str, Field(min_length=1, max_length=256)] | None
    description: Annotated[str, Field(min_length=1, max_length=2048)] | None
    announcement_text: Annotated[str, Field(min_length=1, max_length=2048)] | None
    due_date: datetime | None
    point: Annotated[int, Field(ge=0)] | None
    choices: Annotated[list[str], MinLen(1)] | None


class UpdateClassroomItemModel(BaseModel):
    topic_id: str | None
    attachments_id: Annotated[list[str], MaxLen(8)]
    assigned_to_students_id: list[str] | None
    title: Annotated[str, Field(min_length=1, max_length=256)] | None
    description: Annotated[str, Field(min_length=1, max_length=2048)] | None
    announcement_text: Annotated[str, Field(min_length=1, max_length=2048)] | None
    due_date: datetime | None
    point: Annotated[int, Field(ge=0)] | None
    choices: Annotated[list[str], MinLen(1)] | None

class AddCommentModel(BaseModel):
    comment: Annotated[str, Field(min_length=1, max_length=512)]


class SubmissionModel(BaseModel):
    attachments_id: Annotated[list[str], MaxLen(8)]


class GradeSubmissionModel(BaseModel):
    point: Annotated[int, Field(ge=0)] | None
