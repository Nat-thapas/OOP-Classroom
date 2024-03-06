from typing import BinaryIO

from ..dependencies.dependencies import get_password_hash
from ..exceptions.classroom import InvalidCode, UserAlreadyInClassroom
from ..exceptions.user import EmailAlreadyInUse
from .attachment import Attachment
from .classroom import Classroom
from .user import User


class Controller:
    def __init__(self) -> None:
        self.__users: list[User] = []
        self.__classrooms: list[Classroom] = []
        self.__attachments: list[Attachment] = []

    def create_user(self, username: str, email: str, password: str) -> User:
        if self.get_user_by_email(email) is not None:
            raise EmailAlreadyInUse("Email already in use")
        user = User(username, email, get_password_hash(password))
        self.__users.append(user)
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        for user in self.__users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_email(self, email: str) -> User | None:
        for user in self.__users:
            if user.email == email:
                return user
        return None

    def create_classroom(
        self,
        owner: User,
        name: str,
        section: str | None,
        subject: str | None,
        room: str | None,
    ) -> Classroom:
        classroom = Classroom(owner, name, section, subject, room)
        self.__classrooms.append(classroom)
        return classroom

    def get_classroom_by_id(self, classroom_id: str) -> Classroom | None:
        for classroom in self.__classrooms:
            if classroom.id == classroom_id:
                return classroom
        return None

    def get_classroom_by_code(self, classroom_code: str) -> Classroom | None:
        for classroom in self.__classrooms:
            if classroom.code == classroom_code:
                return classroom
        return None

    def get_classrooms_for_user(self, user: User) -> list[Classroom]:
        classrooms: list[Classroom] = []
        for classroom in self.__classrooms:
            if user in classroom:
                classrooms.append(classroom)
        return classrooms

    def join_classroom_by_code(self, user: User, classroom_code: str) -> Classroom:
        classroom = self.get_classroom_by_code(classroom_code)
        if classroom is None:
            raise InvalidCode("Invalid classroom code")
        if user in classroom:
            raise UserAlreadyInClassroom("User already exist in that classroom")
        classroom.add_student(user)
        return classroom

    def create_attachment(
        self, original_filename: str, content_type: str, data: BinaryIO, owner: User
    ) -> Attachment:
        attachment = Attachment(original_filename, content_type, data, owner)
        self.__attachments.append(attachment)
        return attachment

    def get_attachment_by_id(self, attachment_id: str) -> Attachment | None:
        for attachment in self.__attachments:
            if attachment.id == attachment_id:
                return attachment
        return None


controller = Controller()
