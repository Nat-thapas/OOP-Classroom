from uuid import uuid4

class Topic:
    def __init__(self, name: str) -> None:
        self.__id: str = str(uuid4())
        self.__name: str = name

    @property
    def name(self) -> str:
        return self.__name

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "name": self.__name,
        }
