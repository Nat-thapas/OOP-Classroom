from uuid import uuid4
from datetime import datetime

from .user import User

class Comment:
    def __init__(self, owner: User, text: str) -> None:
        self.__id: str = str(uuid4())
        self.__owner: User = owner
        self.__text: str = text
        self.__created_at: datetime = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "owner": self.__owner.to_dict(),
            "text": self.__text,
            "created_at": self.__created_at.isoformat(),
        }
