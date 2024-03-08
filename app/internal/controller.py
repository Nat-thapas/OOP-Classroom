from typing import BinaryIO

from ..constants.enums import TaskType
from ..exceptions.classroom import InvalidCode, UserAlreadyInClassroom
from ..exceptions.user import EmailAlreadyInUse, UsernameAlreadyInUse
from .attachment import Attachment
from .classroom import Classroom
from .items import Assignment, MultipleChoiceQuestion, Question
from .task import Task, ToDoTask, ToReviewTask
from .user import User


class Controller:
    def __init__(self) -> None:
        self.__users: list[User] = []
        self.__classrooms: list[Classroom] = []
        self.__attachments: list[Attachment] = []

    def create_user(self, username: str, email: str, password_hash: str) -> User:
        if self.get_user_by_email(email) is not None:
            raise EmailAlreadyInUse("Email already in use")
        if self.get_user_by_username(username) is not None:
            raise UsernameAlreadyInUse("Username already in use")
        user = User(username, email, password_hash)
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

    def get_user_by_username(self, username: str) -> User | None:
        for user in self.__users:
            if user.username == username:
                return user
        return None

    def delete_user(self, user: User) -> None:
        if user in self.__users:
            self.__users.remove(user)

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

    def delete_classroom(self, classroom: Classroom) -> None:
        if classroom in self.__classrooms:
            self.__classrooms.remove(classroom)

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

    def get_tasks_for_user(self, user: User, task_type: TaskType) -> list[Task]:
        tasks: list[Task] = []
        if task_type == TaskType.TODO:
            classrooms = self.get_classrooms_for_user(user)
            for classroom in classrooms:
                if user == classroom.owner:
                    continue
                for item in classroom.items:
                    if not isinstance(
                        item, (Assignment, Question, MultipleChoiceQuestion)
                    ):
                        continue
                    tasks.append(ToDoTask(classroom, item, user))
            return tasks
        if task_type == TaskType.TO_REVIEW:
            classrooms = self.get_classrooms_for_user(user)
            for classroom in classrooms:
                if user != classroom.owner:
                    continue
                for item in classroom.items:
                    if not isinstance(
                        item, (Assignment, Question, MultipleChoiceQuestion)
                    ):
                        continue
                    tasks.append(ToReviewTask(classroom, item, user))
            return tasks
        raise ValueError("Invalid task type")


controller = Controller()
