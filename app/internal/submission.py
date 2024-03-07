from uuid import uuid4

from .attachment import Attachment
from .user import User


class Submission:
    def __init__(self, owner: User, attachments: list[Attachment]) -> None:
        self.__id: str = str(uuid4())
        self.__owner: User = owner
        self.__attachments: list[Attachment] = attachments
        self.__point: int | None = None

    @property
    def id(self) -> str:
        return self.__id

    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def point(self) -> int | None:
        return self.__point

    @point.setter
    def point(self, point: int | None) -> None:
        self.__point = point

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "owner_id": self.__owner,
            "point": self.__point,
            "attachments": [
                attachments.to_dict() for attachments in self.__attachments
            ],
        }
