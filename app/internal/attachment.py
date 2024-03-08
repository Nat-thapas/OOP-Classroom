import os
from io import BytesIO
from typing import BinaryIO
from uuid import uuid4

from ..config.config import get_settings
from .user import User

settings = get_settings()


class Attachment:
    def __init__(
        self,
        original_filename: str,
        content_type: str,
        data: BinaryIO,
        owner: User,
    ) -> None:
        self.__id: str = str(uuid4())
        self.__original_filename: str = original_filename
        self.__content_type: str = content_type
        self.__owner: User = owner
        with open(self.__get_path(), "wb") as output_file:
            data.seek(0)
            self.__size: int = output_file.write(data.read())

    def __get_path(self) -> str:
        return os.path.join(settings.attachments_storage_path, self.__id)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def data(self) -> BytesIO:
        with open(self.__get_path(), "rb") as input_file:
            return BytesIO(input_file.read())

    @property
    def path(self) -> str:
        return self.__get_path()

    @property
    def owner(self) -> User:
        return self.__owner

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "name": self.__original_filename,
            "content_type": self.__content_type,
            "owner_id": self.__owner.id,
            "size": self.__size,
        }
