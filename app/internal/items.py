from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from .attachment import Attachment
from .comment import Comment
from .submission import Submission
from .topic import Topic
from .user import User


class BaseItem(ABC):
    def __init__(
        self,
        attachments: list[Attachment],
        assigned_to_students: list[User] | None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._id: str = str(uuid4())
        self._created_at: datetime = datetime.now()
        self._edited_at: datetime = datetime.now()
        self._attachments: list[Attachment] = attachments
        self._assigned_to_students: list[User] | None = assigned_to_students
        self._comments: list[Comment] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def edited_at(self) -> datetime:
        return self._edited_at

    @property
    def attachments(self) -> list[Attachment]:
        return self._attachments

    @property
    def assigned_to_students(self) -> list[User] | None:
        return self._assigned_to_students

    @assigned_to_students.setter
    def assigned_to_students(self, assinged_to_students: list[User] | None) -> None:
        self._edited_at = datetime.now()
        self._assigned_to_students = assinged_to_students

    @attachments.setter
    def attachments(self, attachments: list[Attachment]) -> None:
        self._edited_at = datetime.now()
        self._attachments = attachments

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def create_comment(self, owner: User, text: str) -> Comment:
        comment = Comment(owner, text)
        self._comments.append(comment)
        return comment


class TopicMixin:
    def __init__(self, topic: Topic | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._topic: Topic | None = topic

    @property
    def topic(self) -> Topic | None:
        return self._topic

    @topic.setter
    def topic(self, topic: Topic | None) -> None:
        self._edited_at = datetime.now()
        self._topic = topic


class TitleMixin:
    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._title: str = title

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._edited_at = datetime.now()
        self._title = title


class DescriptionMixin:
    def __init__(self, description: str | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._description: str | None = description

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, description: str | None) -> None:
        self._edited_at = datetime.now()
        self._description = description


class PointMixin:
    def __init__(self, point: int | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._point: int | None = point

    @property
    def point(self) -> int | None:
        return self._point

    @point.setter
    def point(self, point: int | None) -> None:
        self._edited_at = datetime.now()
        self._point = point


class DueDateMixin:
    def __init__(self, due_date: datetime | None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._due_date: datetime | None = due_date

    @property
    def due_date(self) -> datetime | None:
        return self._due_date

    @due_date.setter
    def due_date(self, due_date: datetime | None) -> None:
        self._edited_at = datetime.now()
        self._due_date = due_date


class SubmissionsMixin:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._submissions: list[Submission] = []

    @property
    def submissions(self) -> list[Submission]:
        return self._submissions

    def create_submission(
        self, user: User, attachments: list[Attachment]
    ) -> Submission:
        submission = Submission(user, attachments)
        self._submissions.append(submission)
        return submission

    def get_submission_by_id(self, submission_id: str) -> Submission | None:
        for submission in self._submissions:
            if submission.id == submission_id:
                return submission
        return None

    def get_submission_by_owner(self, owner: User) -> Submission | None:
        for submission in self._submissions:
            if submission.owner == owner:
                return submission
        return None

    def delete_submission(self, submission: Submission) -> bool:
        if submission not in self._submissions:
            return False
        self._submissions.remove(submission)
        return True


class Announcement(BaseItem):
    def __init__(
        self,
        attachments: list[Attachment],
        assigned_to_students: list[User] | None,
        announcement_text: str,
    ) -> None:
        super().__init__(
            attachments=attachments,
            assigned_to_students=assigned_to_students,
        )
        self.__announcement_text: str = announcement_text

    @property
    def announcement_text(self) -> str:
        return self.__announcement_text

    @announcement_text.setter
    def announcement_text(self, announcement_text: str) -> None:
        self._edited_at = datetime.now()
        self.__announcement_text = announcement_text

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "type": "Announcement",
            "created_at": self._created_at.isoformat(),
            "edited_at": self._edited_at.isoformat(),
            "attachments": [attachment.to_dict() for attachment in self._attachments],
            "announcement_text": self.__announcement_text,
            "comments": [comment.to_dict() for comment in self._comments],
        }


class Material(TopicMixin, TitleMixin, DescriptionMixin, BaseItem):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User] | None,
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
            "id": self._id,
            "type": "Material",
            "created_at": self._created_at.isoformat(),
            "edited_at": self._edited_at.isoformat(),
            "attachments": [attachment.to_dict() for attachment in self._attachments],
            "topic": self._topic.to_dict() if self._topic else None,
            "title": self._title,
            "description": self._description,
            "comments": [comment.to_dict() for comment in self._comments],
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
        assigned_to_students: list[User] | None,
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
            "id": self._id,
            "type": "Assignment",
            "created_at": self._created_at.isoformat(),
            "edited_at": self._edited_at.isoformat(),
            "attachments": [attachment.to_dict() for attachment in self._attachments],
            "topic": self._topic.to_dict() if self._topic else None,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "point": self._point,
            "comments": [comment.to_dict() for comment in self._comments],
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
        assigned_to_students: list[User] | None,
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
            "id": self._id,
            "type": "Question",
            "created_at": self._created_at.isoformat(),
            "edited_at": self._edited_at.isoformat(),
            "attachments": [attachment.to_dict() for attachment in self._attachments],
            "topic": self._topic.to_dict() if self._topic else None,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "point": self._point,
            "comments": [comment.to_dict() for comment in self._comments],
        }


class MultipleChoiceQuestion(Question):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User] | None,
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
        choices: list[str],
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
        self.__choices: list[str] = choices

    @property
    def choices(self) -> list[str]:
        return self.__choices

    @choices.setter
    def choices(self, choices: list[str]) -> None:
        self._edited_at = datetime.now()
        self.__choices = choices

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "type": "MultipleChoiceQuestion",
            "created_at": self._created_at.isoformat(),
            "edited_at": self._edited_at.isoformat(),
            "attachments": [attachment.to_dict() for attachment in self._attachments],
            "topic": self._topic.to_dict() if self._topic else None,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "point": self._point,
            "choices": self.__choices,
            "comments": [comment.to_dict() for comment in self._comments],
        }
