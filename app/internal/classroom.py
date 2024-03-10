import os
import random
from datetime import datetime
from functools import lru_cache
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


@lru_cache
def get_valid_banner_images() -> list[str]:
    banner_categories = os.listdir(settings.banner_images_storage_path)
    banner_images: list[str] = []
    for category in banner_categories:
        category_path = os.path.join(settings.banner_images_storage_path, category)
        for image in os.listdir(category_path):
            banner_images.append(f"static/banner-images/{category}/{image}")
    return banner_images


@lru_cache
def get_general_banner_images() -> list[str]:
    banner_images: list[str] = []
    category = "General"
    category_path = os.path.join(settings.banner_images_storage_path, category)
    for image in os.listdir(category_path):
        banner_images.append(f"static/banner-images/{category}/{image}")
    return banner_images


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
        self.__banner_path: str = random.choice(get_general_banner_images())
        if "Honors" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[7]
        elif "Breakfast" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[3]
        elif "Graduation" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[6]
        elif "Code" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[7]
        elif "Bookclub" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[1]
        elif "Reachout" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[1]
        elif "LearnLanguage" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[0]
        elif "BackToSchool" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[4]
        elif "Read" in self.__banner_path:
            self.__theme_color: str = settings.theme_colors[7]
        else:
            self.__theme_color: str = random.choice(settings.theme_colors)

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
    def name(self) -> str:
        return self.__name

    @property
    def section(self) -> str | None:
        return self.__section

    @property
    def subject(self) -> str | None:
        return self.__subject

    @property
    def room(self) -> str | None:
        return self.__room

    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def code(self) -> str:
        return self.__code

    @property
    def students(self) -> list[User]:
        return self.__students

    @property
    def topics(self) -> list[Topic]:
        return self.__topics

    @property
    def items(self) -> list[BaseItem]:
        return self.__items

    @property
    def banner_path(self) -> str:
        return self.__banner_path

    @property
    def theme_color(self) -> str:
        return self.__theme_color

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @section.setter
    def section(self, section: str | None) -> None:
        self.__section = section

    @subject.setter
    def subject(self, subject: str | None) -> None:
        self.__subject = subject

    @room.setter
    def room(self, room: str | None) -> None:
        self.__room = room

    @banner_path.setter
    def banner_path(self, banner_path: str) -> None:
        if banner_path not in get_valid_banner_images():
            raise ValueError("Invalid banner path")
        self.__banner_path = banner_path

    @theme_color.setter
    def theme_color(self, theme_color: str) -> None:
        if theme_color not in settings.theme_colors:
            raise ValueError("Invalid theme color")
        self.__theme_color = theme_color

    def to_dict(
        self,
        include_code: bool = False,
        include_lists: bool = False,
        filter_item_for_user: User | None = None,
    ) -> dict:
        classroom_dict: dict = {
            "id": self.__id,
            "owner": self.__owner.to_dict(),
            "name": self.__name,
            "section": self.__section,
            "subject": self.__subject,
            "room": self.__room,
            "banner_path": self.__banner_path,
            "theme_color": self.__theme_color,
        }
        if include_code:
            classroom_dict["code"] = self.__code

        if include_lists:
            classroom_dict["students"] = [
                student.to_dict() for student in self.__students
            ]
            classroom_dict["topics"] = [topic.to_dict() for topic in self.__topics]
            if filter_item_for_user and filter_item_for_user != self.__owner:
                classroom_dict["items"] = [
                    item.to_dict()
                    for item in self.__items
                    if item.assigned_to_students is None
                    or filter_item_for_user in item.assigned_to_students
                ]
            else:
                classroom_dict["items"] = [item.to_dict() for item in self.__items]

        return classroom_dict

    def create_topic(self, name: str) -> Topic:
        topic = Topic(name)
        self.__topics.append(topic)
        return topic

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
        assigned_to_students: list[User] | None,
        announcement_text: str,
    ):
        if assigned_to_students:
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
        assigned_to_students: list[User] | None,
        title: str,
        description: str | None,
    ):
        if topic and topic not in self.__topics:
            raise ValueError("Invalid topic")
        if assigned_to_students:
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
        assigned_to_students: list[User] | None,
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
    ):
        if topic and topic not in self.__topics:
            raise ValueError("Invalid topic")
        if assigned_to_students:
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
        assigned_to_students: list[User] | None,
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
    ):
        if topic and topic not in self.__topics:
            raise ValueError("Invalid topic")
        if assigned_to_students:
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
        assigned_to_students: list[User] | None,
        title: str,
        description: str | None,
        due_date: datetime | None,
        point: int | None,
        choices: list[str],
    ):
        if topic and topic not in self.__topics:
            raise ValueError("Invalid topic")
        if assigned_to_students:
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

    def delete_item(self, item: BaseItem) -> bool:
        if item not in self.__items:
            return False
        self.__items.remove(item)
        return True
