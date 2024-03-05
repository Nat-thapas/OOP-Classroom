import random

from uuid import uuid4

from .user import User
from ..config.config import get_settings

from .topic import Topic
from .rubric import Rubric
from .items import Announcement, Material, Assignment, Question, MultipleChoiceQuestion

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
        self.__rubrics: list[Rubric] = []
        self.__items: list[
            Announcement | Material | Assignment | Question | MultipleChoiceQuestion
        ] = []
