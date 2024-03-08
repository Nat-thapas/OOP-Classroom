import os
from hashlib import sha1
from io import BytesIO
from uuid import uuid4

import pydenticon

from ..config.config import get_settings

settings = get_settings()


IDENTICON_FORGROUND_COLORS = [
    "rgb(45,79,255)",
    "rgb(254,180,44)",
    "rgb(226,121,234)",
    "rgb(30,179,253)",
    "rgb(232,77,65)",
    "rgb(49,203,115)",
    "rgb(141,69,170)",
]

IDENTICON_BACKGROUND_COLOR = "rgb(224,224,224)"

IDENTICON_PADDING = (24, 24, 24, 24)

identicon_generator = pydenticon.Generator(
    rows=5,
    columns=5,
    digest=sha1,
    foreground=IDENTICON_FORGROUND_COLORS,
    background=IDENTICON_BACKGROUND_COLOR,
)


class Avatar:
    def __init__(self) -> None:
        self.__id: str = str(uuid4())
        identicon = identicon_generator.generate(
            self.__id, 256, 256, padding=IDENTICON_PADDING, output_format="png"
        )
        self.__content_type: str = "image/png"
        with open(self.__get_path(), "wb") as output_file:
            self.__size: int = output_file.write(identicon)  # type: ignore

    def __get_path(self) -> str:
        return os.path.join(settings.avatar_images_storage_path, self.__id)

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

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "content_type": self.__content_type,
            "size": self.__size,
        }
