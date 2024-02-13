import logging
import time
from datetime import datetime

from user import User


class TopicAlreadyExist(Exception):
    pass


class Topic:
    def __init__(self, name: str) -> None:
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
        self.__topic: Topic = topic
        self.__time_created: float = time.time()
        self.__attachments: list[Attachment] | None = attachments
        self.__assigned_to: list[User] | None = assigned_to


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
    def __init__(self, name: str, section: str, subject: str, room: str) -> None:
        self.__name: str = name
        self.__section: str = section
        self.__subject: str = subject
        self.__room: str = room
        self.__topics: list[Topic] = []
        self.__rubrics: list[Rubric] = []
        self.__items: list[Announcement | Assignment | Question | Material] = []

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
    ):
        announcement: Announcement = Announcement(
            topic, attachments, assigned_to, announcement_text
        )
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
    ):
        assignment: Assignment = Assignment(
            topic, attachments, assigned_to, title, instruction, due_date, point, rubric
        )
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
    ):
        question: Question = Question(
            topic, attachments, assigned_to, question_text, instruction, due_date, point
        )
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
    ):
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
        self.__items.append(question)

    def add_material(
        self,
        topic: Topic,
        attachments: list[Attachment] | None,
        assigned_to: list[User] | None,
        title: str,
        description: str | None,
    ):
        material: Material = Material(
            topic, attachments, assigned_to, title, description
        )
        self.__items.append(material)

    @property
    def topics(self):
        return self.__topics
