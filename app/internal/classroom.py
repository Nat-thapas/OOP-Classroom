import random
from datetime import datetime
from uuid import uuid4

from ..config.config import get_settings
from .attachment import Attachment
from .items import (
    Announcement,
    Assignment,
    BaseItem,
    Material,
    MultipleChoiceQuestion,
    Question,
)
from .topic import Topic
from .user import User

settings = get_settings()


class Classroom:
    def __init__(
        self,
        owner: User,
        name: str,
        section: str | None,
        subject: str | None,
        room: str | None,
    ) -> None:
        self.__id: str = str(uuid4())
        self.__owner: User = owner
        self.__name: str = name
        self.__section: str | None = section
        self.__subject: str | None = subject
        self.__room: str | None = room
        self.__code: str = "".join(
            random.choices(
                "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=settings.classroom_code_length
            )
        )
        self.__students: list[User] = []
        self.__topics: list[Topic] = []
        self.__items: list[BaseItem] = []

    def __contains__(self, item: User | Topic | BaseItem) -> bool:
        if item == self.__owner:
            return True
        if item in self.__students:
            return True
        if item in self.__topics:
            return True
        if item in self.__items:
            return True
        return False

    @property
    def id(self) -> str:
        return self.__id

    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def code(self) -> str:
        return self.__code

    @property
    def items(self) -> list[BaseItem]:
        return self.__items

    def to_dict(self, include_code: bool = False, include_lists: bool = False) -> dict:
        classroom_dict: dict = {
            "id": self.__id,
            "owner_id": self.__owner.id,
            "name": self.__name,
            "section": self.__section,
            "subject": self.__subject,
            "room": self.__room,
        }
        if include_code:
            classroom_dict["code"] = self.__code

        if include_lists:
            classroom_dict["students"] = [
                student.to_dict() for student in self.__students
            ]
            classroom_dict["topics"] = [topic.to_dict() for topic in self.__topics]
            classroom_dict["items"] = [item.to_dict() for item in self.__items]

        return classroom_dict

    def get_topic_by_id(self, topic_id: str) -> Topic | None:
        for topic in self.__topics:
            if topic.id == topic_id:
                return topic
        return None

    def get_item_by_id(self, item_id: str) -> BaseItem | None:
        for item in self.__items:
            if item.id == item_id:
                return item
        return None

    def add_student(self, student: User) -> bool:
        if student == self.__owner:
            return False
        if student in self.__students:
            return False
        self.__students.append(student)
        return True

    def create_announcement(
        self,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        announcement_text: str,
    ):
        for student in assigned_to_students:
            if student not in self.__students:
                raise ValueError("Invalid student")
        announcement = Announcement(
            attachments, assigned_to_students, announcement_text
        )
        self.__items.append(announcement)
        return announcement

    def create_material(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
    ):
        if topic not in self.__topics:
            raise ValueError("Invalid topic")
        for student in assigned_to_students:
            if student not in self.__students:
                raise ValueError("Invalid student")
        material = Material(
            topic, attachments, assigned_to_students, title, description
        )
        self.__items.append(material)
        return material

    def create_assignment(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
    ):
        if topic not in self.__topics:
            raise ValueError("Invalid topic")
        for student in assigned_to_students:
            if student not in self.__students:
                raise ValueError("Invalid student")
        assignment = Assignment(
            topic,
            attachments,
            assigned_to_students,
            title,
            description,
            due_date,
            point,
        )
        self.__items.append(assignment)
        return assignment

    def create_question(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
    ):
        if topic not in self.__topics:
            raise ValueError("Invalid topic")
        for student in assigned_to_students:
            if student not in self.__students:
                raise ValueError("Invalid student")
        question = Question(
            topic,
            attachments,
            assigned_to_students,
            title,
            description,
            due_date,
            point,
        )
        self.__items.append(question)
        return question

    def create_multiple_choice_question(
        self,
        topic: Topic | None,
        attachments: list[Attachment],
        assigned_to_students: list[User],
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
        choices: list[str]
    ):
        if topic not in self.__topics:
            raise ValueError("Invalid topic")
        for student in assigned_to_students:
            if student not in self.__students:
                raise ValueError("Invalid student")
        multiple_choice_question = MultipleChoiceQuestion(
            topic,
            attachments,
            assigned_to_students,
            title,
            description,
            due_date,
            point,
            choices,
        )
        self.__items.append(multiple_choice_question)
        return multiple_choice_question