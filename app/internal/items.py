from uuid import uuid4
from datetime import datetime
from abc import ABC, abstractmethod

from .user import User
from .attachment import Attachment
from .submission import Submission
from .topic import Topic
from .rubric import Rubric


class BaseItem(ABC):
    def __init__(
        self, attachments: list[Attachment], assigned_to_students: list[User], **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__id: str = str(uuid4())
        self.__time_created: datetime = datetime.now()
        self.__time_edited: datetime = datetime.now()
        self.__attachments: list[Attachment] = attachments
        self.__assigned_to_students: list[User] = assigned_to_students

    @property
    def id(self) -> str:
        return self.__id

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class TopicMixin:
    def __init__(self, topic: Topic | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__topic: Topic | None = topic

    @property
    def topic(self) -> Topic | None:
        return self.__topic


class TitleMixin:
    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__title: str = title

    @property
    def title(self) -> str:
        return self.__title


class DescriptionMixin:
    def __init__(self, description: str | None, **kwargs) -> None:
        super().__init__(*kwargs)
        self.__description: str | None = description

    @property
    def description(self) -> str | None:
        return self.__description


class PointMixin:
    def __init__(self, point: int | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__point: int | None = point

    @property
    def point(self) -> int | None:
        return self.__point


class RubricMixin:
    def __init__(self, rubric: Rubric | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__rubric: Rubric | None = rubric

    @property
    def rubric(self) -> Rubric | None:
        return self.__rubric


class DueDateMixin:
    def __init__(self, due_date: datetime | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__due_date: datetime | None = due_date

    @property
    def due_date(self) -> datetime | None:
        return self.__due_date


class SubmissionsMixin:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__submissions: dict[User, Submission] = {}

    @property
    def submissions(self) -> dict[User, Submission]:
        return self.__submissions


class Announcement(BaseItem):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        announcement_text: str,
    ) -> None:
        super().__init__(
            topic=topic,
            attachments=attachments,
            assigned_to_students=assigned_to_students,
        )
        self.__announcement_text: str = announcement_text

    @property
    def announcement_text(self) -> str:
        return self.__announcement_text

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "time_created": self.__time_created,
            "time_edited": self.__time_edited,
            "attachments": [attachment.to_dict() for attachment in self.__attachments],
            "announcement_text": self.__announcement_text,
        }


class Material(TopicMixin, TitleMixin, DescriptionMixin, BaseItem):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
    ):
        super().__init__(
            topic=topic,
            attachments=attachments,
            assigned_to_students=assigned_to_students,
            title=title,
            description=description,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "time_created": self.__time_created,
            "time_edited": self.__time_edited,
            "attachments": [attachment.to_dict() for attachment in self.__attachments],
            "topic": self.__topic.to_dict() if self.__topic else "",
            "title": self.__title,
            "description": self.__description,
        }


class Assignment(
    TopicMixin,
    TitleMixin,
    DescriptionMixin,
    DueDateMixin,
    PointMixin,
    SubmissionsMixin,
    BaseItem,
):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
    ):
        super().__init__(
            topic=topic,
            attachments=attachments,
            assigned_to_students=assigned_to_students,
            title=title,
            description=description,
            due_date=due_date,
            point=point,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "time_created": self.__time_created,
            "time_edited": self.__time_edited,
            "attachments": [attachment.to_dict() for attachment in self.__attachments],
            "topic": self.__topic.to_dict() if self.__topic else "",
            "title": self.__title,
            "description": self.__description,
            "due_date": self.__due_date,
            "point": self.__point,
        }


class Question(
    TopicMixin,
    TitleMixin,
    DescriptionMixin,
    DueDateMixin,
    PointMixin,
    SubmissionsMixin,
    BaseItem,
):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
    ):
        super().__init__(
            topic=topic,
            attachments=attachments,
            assigned_to_students=assigned_to_students,
            title=title,
            description=description,
            due_date=due_date,
            point=point,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "time_created": self.__time_created,
            "time_edited": self.__time_edited,
            "attachments": [attachment.to_dict() for attachment in self.__attachments],
            "topic": self.__topic.to_dict() if self.__topic else "",
            "title": self.__title,
            "description": self.__description,
            "due_date": self.__due_date,
            "point": self.__point,
        }

class MultipleChoiceQuestion(Question):
    pass
