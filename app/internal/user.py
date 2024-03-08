from uuid import uuid4

from .avatar import Avatar


class User:
    def __init__(self, username: str, email: str, hashed_password: str) -> None:
        self.__id: str = str(uuid4())
        self.__username: str = username
        self.__email: str = email
        self.__hashed_password: str = hashed_password
        self.__avatar: Avatar = Avatar()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def email(self) -> str:
        return self.__email

    @property
    def hashed_password(self) -> str:
        return self.__hashed_password

    @property
    def avatar(self) -> Avatar:
        return self.__avatar

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @email.setter
    def email(self, email: str) -> None:
        self.__email = email

    @hashed_password.setter
    def hashed_password(self, hashed_password: str) -> None:
        self.__hashed_password = hashed_password

    def to_dict(self):
        return {
            "id": self.__id,
            "username": self.__username,
            "email": self.__email,
            "avatar": self.__avatar.to_dict(),
        }
