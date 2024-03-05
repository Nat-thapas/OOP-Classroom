import os
from io import BytesIO
from uuid import uuid4

from ..config.config import get_settings

settings = get_settings()


class Attachment:
    def __init__(self, data: BytesIO) -> None:
        self.__id: str = str(uuid4())
        with open(self.__get_path(), "wb") as file:
            data.seek(0)
            self.__size: int = file.write(data.getbuffer())

    def __get_path(self) -> str:
        return os.path.join(settings.file_storage_path, self.__id)

    @property
    def data(self) -> BytesIO:
        with open(self.__get_path(), "rb") as file:
            return BytesIO(file.read())

    @property
    def path(self) -> str:
        return self.__get_path()

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "size": self.__size,
        }
