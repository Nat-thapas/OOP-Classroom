import logging
import time
import random
import os
from uuid import uuid4
from datetime import datetime
from typing import Sequence

from user import User


CLASSROOM_CODE_LENGTH = int(os.getenv("CLASSROOM_CODE_LENGTH", "8"))


class TopicAlreadyExist(Exception):
    pass


class Topic:
    def __init__(self, name: str) -> None:
        self.__id: str = str(uuid4())
        self.__name: str = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name


class Attachment:
    pass


class Rubric:
    def __init__(self, name: str) -> None:
        self.__id: str = str(uuid4())
        self.__name: str = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name


class Item:
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
    ) -> None:
        self.__id: str = str(uuid4())
        self.__topic: Topic | None = topic
        self.__time_created: float = time.time()
        self.__attachments: list[Attachment] | None = attachments
        self.__assigned_to: list[User] | None = assigned_to

    @property
    def id(self):
        return self.__id
    
    def base_dict(self):
        return {
            "id": self.__id,
            "topic": self.__topic,
            "time_created": self.__time_created,
            "attachments": ["TODO: Implement this" for attachment in self.__attachments] if self.__attachments else None,
            "assigned_to": [user.id for user in self.__assigned_to] if self.__assigned_to else None
        }
    
    def dict(self):
        return self.base_dict()


class Announcement(Item):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        announcement_text: str,
    ) -> None:
        super().__init__(topic, attachments, assigned_to)
        self.__announcement_text: str = announcement_text

    def dict(self):
        data_dict = self.base_dict()
        data_dict["announcement_text"] = self.__announcement_text
        return data_dict


class Assignment(Item):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
        rubric: Rubric | None,
    ) -> None:
        super().__init__(topic, attachments, assigned_to)
        self.__title: str = title
        self.__instruction: str | None = instruction
        self.__due_date: datetime | None = due_date
        self.__point: int | None = point
        self.__rubric: Rubric | None = rubric

    def dict(self):
        data_dict = self.base_dict()
        data_dict["title"] = self.__title
        data_dict["instruction"] = self.__instruction
        data_dict["due_date"] = self.__due_date.timestamp() if self.__due_date else None
        data_dict["point"] = self.__point
        data_dict["rubric"] = None # self.__rubric.dict()
        return data_dict


class Question(Item):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        question_text: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
    ) -> None:
        super().__init__(topic, attachments, assigned_to)
        self.__question_text: str = question_text
        self.__instruction: str | None = instruction
        self.__due_date: datetime | None = due_date
        self.__point: int | None = point

    def dict(self):
        data_dict = self.base_dict()
        data_dict["question_text"] = self.__question_text
        data_dict["instruction"] = self.__instruction
        data_dict["due_date"] = self.__due_date.timestamp() if self.__due_date else None
        data_dict["point"] = self.__point
        return data_dict


class MultipleChoiceQuestion(Question):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        question_text: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
        choices: list[str],
    ) -> None:
        super().__init__(
            topic, attachments, assigned_to, question_text, instruction, due_date, point
        )
        self.__choices: list[str] = choices

    def dict(self):
        data_dict = self.base_dict()
        data_dict["choices"] = [choice for choice in self.__choices]
        return data_dict


class Material(Item):
    def __init__(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        description: str | None,
    ) -> None:
        super().__init__(topic, attachments, assigned_to)
        self.__title: str = title
        self.__description: str | None = description

    def dict(self):
        data_dict = self.base_dict()
        data_dict["title"] = self.__title
        data_dict["description"] = self.__description
        return data_dict


class Classroom:
    def __init__(self, owner: User, name: str, section: str | None, subject: str | None, room: str | None) -> None:
        self.__id: str = str(uuid4())
        self.__owner: User = owner
        self.__name: str = name
        self.__section: str | None = section
        self.__subject: str | None = subject
        self.__room: str | None = room
        self.__code: str = ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=CLASSROOM_CODE_LENGTH))
        self.__students: list[User] = []
        self.__topics: list[Topic] = []
        self.__rubrics: list[Rubric] = []
        self.__items: list[Announcement | Assignment | Question | Material] = []

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def owner(self) -> User:
        return self.__owner
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def students(self) -> list[User]:
        return self.__students
    
    @property
    def items(self) -> Sequence[Item]:
        return self.__items
    
    def short_dict(self, user: User) -> dict[str, str | list[str]]:
        if user != self.__owner and user not in self.__students:
            logging.info(f"User: {user.name} requested for but is not in classroom: {self.__name}")
            raise PermissionError("User not in classroom")
        return {
            "id": self.__id,
            "owner_id": self.__owner.id,
            "owner_name": self.__owner.name,
            "name": self.__name,
            "section": self.__section or "",
            "subject": self.__subject or "",
            "room": self.__room or "",
            "code": self.__code if user == self.__owner else "",
        }
    
    def long_dict(self, user: User) -> dict[str, str | list[str]]:
        if user != self.__owner and user not in self.__students:
            logging.info(f"User: {user.name} requested for but is not in classroom: {self.__name}")
            raise PermissionError("User not in classroom")
        return {
            "id": self.__id,
            "owner_id": self.__owner.id,
            "name": self.__name,
            "section": self.__section or "",
            "subject": self.__subject or "",
            "room": self.__room or "",
            "code": self.__code if user == self.__owner else "",
            "students": [student.id for student in self.__students],
            "items": [item.id for item in self.__items],
        }
    
    def verify_user(self, user: User) -> bool:
        if user != self.__owner and user not in self.__students:
            logging.info(f"User: {user.name} requested for but is not in classroom: {self.__name}")
            raise PermissionError("User not in classroom")
        return True
    
    def get_topic(self, id: str) -> Topic:
        for topic in self.__topics:
            if topic.id == id:
                return topic
        raise LookupError("Topic not found")
    
    def get_rubric(self, id: str) -> Rubric:
        for rubric in self.__rubrics:
            if rubric.id == id:
                return rubric
        raise LookupError("Rubric not found")

    def add_student(self, student: User) -> bool:
        if student in self.__students:
            logging.info(f"Student: {student.name} is already in classroom: {self.__name}")
            return False
        self.__students.append(student)
        logging.info(f"Added student: {student.name} to classroom: {self.__name}")
        return True

    def add_topic(self, name: str) -> Topic:
        for topic in self.__topics:
            if topic.name == name:
                logging.info(f"Topic: {name} already exist in classroom: {self.__name}")
                raise TopicAlreadyExist("Topic already exist")
        logging.info(f"Creating topic: {name} for classroom: {self.__name}")
        topic: Topic = Topic(name)
        self.__topics.append(topic)
        return topic

    def add_announcement(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        announcement_text: str,
    ) -> Announcement:
        announcement: Announcement = Announcement(
            topic, attachments, assigned_to, announcement_text
        )
        logging.info(f"Added announcement: {topic} to classroom: {self.__name}")
        self.__items.append(announcement)
        return announcement

    def add_assignment(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
        rubric: Rubric | None,
    ) -> Assignment:
        assignment: Assignment = Assignment(
            topic, attachments, assigned_to, title, instruction, due_date, point, rubric
        )
        logging.info(f"Added assignment: {topic} to classroom: {self.__name}")
        self.__items.append(assignment)
        return assignment

    def add_question(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        question_text: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
    ) -> Question:
        question: Question = Question(
            topic, attachments, assigned_to, question_text, instruction, due_date, point
        )
        logging.info(f"Added question: {topic} to classroom: {self.__name}")
        self.__items.append(question)
        return question

    def add_multiple_choice_question(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        question_text: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
        choices: list[str],
    ) -> MultipleChoiceQuestion:
        question: MultipleChoiceQuestion = MultipleChoiceQuestion(
            topic,
            attachments,
            assigned_to,
            question_text,
            instruction,
            due_date,
            point,
            choices,
        )
        logging.info(f"Added multiple choices questions: {topic} to classroom: {self.__name}")
        self.__items.append(question)
        return question

    def add_material(
        self,
        topic: Topic | None,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        description: str | None,
    ) -> Material:
        material: Material = Material(
            topic, attachments, assigned_to, title, description
        )
        logging.info(f"Added material: {topic} to classroom: {self.__name}")
        self.__items.append(material)
        return material

    def get_item(self, id: str) -> Item:
        for item in self.__items:
            if item.id == id:
                return item
        raise LookupError("Item not found")

    @property
    def topics(self) -> list[Topic]:
        return self.__topics