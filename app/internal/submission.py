from uuid import uuid4

from .attachment import Attachment
from .comment import Comment
from .user import User


class Submission:
    def __init__(self, owner: User, attachments: list[Attachment]) -> None:
        self.__id: str = str(uuid4())
        self.__owner: User = owner
        self.__attachments: list[Attachment] = attachments
        self.__point: int | None = None
        self.__comments: list[Comment] = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def attachments(self) -> list[Attachment]:
        return self.__attachments

    @property
    def point(self) -> int | None:
        return self.__point

    @attachments.setter
    def attachments(self, attachments: list[Attachment]) -> None:
        self.__attachments = attachments

    @point.setter
    def point(self, point: int | None) -> None:
        self.__point = point

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "owner": self.__owner.to_dict(),
            "point": self.__point,
            "attachments": [attachment.to_dict() for attachment in self.__attachments],
            "comments": [comment.to_dict() for comment in self.__comments],
        }

    def create_comment(self, owner: User, text: str) -> Comment:
        comment = Comment(owner, text)
        self.__comments.append(comment)
        return comment
