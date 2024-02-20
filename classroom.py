import logging
import time
import random
import os
from uuid import uuid4
from datetime import datetime

from user import User


CLASSROOM_CODE_LENGTH = int(os.getenv("CLASSROOM_CODE_LENGTH", "8"))


class TopicAlreadyExist(Exception):
    pass


class Topic:
    def __init__(self, name: str) -> None:
        self.__id: str = str(uuid4())
        self.__name: str = name

    @property
    def name(self):
        return self.__name


class Attachment:
    pass


class Rubric:
    pass


class Item:
    def __init__(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
    ) -> None:
        self.__id: str = str(uuid4())
        self.__topic: Topic = topic
        self.__time_created: float = time.time()
        self.__attachments: list[Attachment] | None = attachments
        self.__assigned_to: list[User] | None = assigned_to

    @property
    def id(self):
        return self.__id


class Announcement(Item):
    def __init__(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        announcement_text: str,
    ) -> None:
        super().__init__(topic, attachments, assigned_to)
        self.__announcement_text: str = announcement_text


class Assignment(Item):
    def __init__(
        self,
        topic: Topic,
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


class Question(Item):
    def __init__(
        self,
        topic: Topic,
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


class MultipleChoiceQuestion(Question):
    def __init__(
        self,
        topic: Topic,
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


class Material(Item):
    def __init__(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        description: str | None,
    ) -> None:
        super().__init__(topic, attachments, assigned_to)
        self.__title: str = title
        self.__description: str | None = description


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
        }
    
    def long_dict(self, user: User) -> dict[str, str | list[str]]:
        if user != self.__owner and user not in self.__students:
            logging.info(f"User: {user.name} requested for but is not in classroom: {self.__name}")
            raise PermissionError("User not in classroom")
        return {
            "id": self.__id,
            "owner_id": self.__owner.id, # TODO: Change to user dict
            "name": self.__name,
            "section": self.__section or "",
            "subject": self.__subject or "",
            "room": self.__room or "",
            "code": self.__code if user == self.__owner else "",
            "students": [student.id for student in self.__students],
            "items": [item.id for item in self.__items],
        }
    
    def add_student(self, student: User) -> bool:
        if student in self.__students:
            logging.info(f"Student: {student.name} is already in classroom: {self.__name}")
            return False
        self.__students.append(student)
        logging.info(f"Added student: {student.name} to classroom: {self.__name}")
        return True

    def add_topic(self, name: str) -> None:
        for topic in self.__topics:
            if topic.name == name:
                logging.info(f"Topic: {name} already exist in classroom: {self.__name}")
                raise TopicAlreadyExist("Topic already exist")
        logging.info(f"Creating topic: {name} for classroom: {self.__name}")
        self.__topics.append(Topic(name))

    def add_announcement(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        announcement_text: str,
    ) -> None:
        announcement: Announcement = Announcement(
            topic, attachments, assigned_to, announcement_text
        )
        logging.info(f"Added announcement: {topic} to classroom: {self.__name}")
        self.__items.append(announcement)

    def add_assignment(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
        rubric: Rubric | None,
    ) -> None:
        assignment: Assignment = Assignment(
            topic, attachments, assigned_to, title, instruction, due_date, point, rubric
        )
        logging.info(f"Added assignment: {topic} to classroom: {self.__name}")
        self.__items.append(assignment)

    def add_question(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        question_text: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
    ) -> None:
        question: Question = Question(
            topic, attachments, assigned_to, question_text, instruction, due_date, point
        )
        logging.info(f"Added question: {topic} to classroom: {self.__name}")
        self.__items.append(question)

    def add_multiple_choice_question(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        question_text: str,
        instruction: str | None,
        due_date: datetime | None,
        point: int | None,
        choices: list[str],
    ) -> None:
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

    def add_material(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        description: str | None,
    ) -> None:
        material: Material = Material(
            topic, attachments, assigned_to, title, description
        )
        logging.info(f"Added material: {topic} to classroom: {self.__name}")
        self.__items.append(material)

    @property
    def topics(self) -> list[Topic]:
        return self.__topics
