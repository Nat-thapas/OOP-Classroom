import logging

from classroom import Classroom
from session import Session
from user import User


class InvalidCredential(Exception):
    pass


class EmailAlreadyInUse(Exception):
    pass


class InvalidClassroomCode(Exception):
    pass


class AlreadyInClassroom(Exception):
    pass


class Controller:
    def __init__(self) -> None:
        self.__sessions_controller: Session = Session()
        self.__users: list[User] = []
        self.__classrooms: list[Classroom] = []

    def register(self, name: str, email: str, password: str) -> str:
        logging.info(f"Registering user with email: {email}")
        for user in self.__users:
            if user.email == email:
                logging.info(f"Email: {email} is already in use")
                raise EmailAlreadyInUse("Email is already in use")
        user: User = User(name, email, password)
        self.__users.append(user)
        token: str = self.__sessions_controller.add_user(user)
        logging.info(f"Registeration of user with email: {email} succeeded")
        return token

    def login(self, email: str, password: str) -> str:
        logging.info(f"User with email: {email} is trying to login")
        for user in self.__users:
            if user.email == email and user.check_password(password):
                token: str = self.__sessions_controller.add_user(user)
                logging.info(f"User with email: {email} successfully logged in")
                return token
        logging.info(f"User with email: {email} failed to login")
        raise InvalidCredential("Email or password is incorrect")
    
    def get_user(self, id: str) -> User:
        for user in self.__users:
            if user.id == id:
                return user
        raise LookupError("User not found")

    def get_user_from_token(self, token: str) -> User:
        return self.__sessions_controller.get_user(token)

    def check_token(self, token: str) -> bool:
        return self.__sessions_controller.check_token(token)

    def get_classrooms_for_user(self, user: User) -> list[Classroom]:
        classrooms: list[Classroom] = []
        for classroom in self.__classrooms:
            if classroom.owner == user or user in classroom.students:
                classrooms.append(classroom)
        return classrooms
    
    def get_classroom(self, id: str) -> Classroom:
        for classroom in self.__classrooms:
            if classroom.id == id:
                return classroom
        logging.info(f"Failed to lookup classroom with ID: {id}")
        raise LookupError(f"Classroom with ID: {id} not found")

    def create_classroom(
        self,
        user: User,
        name: str,
        section: str | None,
        subject: str | None,
        room: str | None,
    ) -> str:
        classroom: Classroom = Classroom(user, name, section, subject, room)
        self.__classrooms.append(classroom)
        logging.info(f"Created classroom with id: {classroom.id}")
        return classroom.id

    def join_classroom(self, user: User, code: str) -> str:
        for classroom in self.__classrooms:
            if classroom.code == code:
                if classroom.owner == user:
                    raise AlreadyInClassroom("User is the owner of the class")
                if user in classroom.students:
                    raise AlreadyInClassroom("User is a student of the class")
                classroom.add_student(user)
                logging.info(f"User: {user.name} successfully join classroom: {classroom.name} with code")
                return classroom.id
        logging.info(f"User: {user.name} failed to join classroom with code: {code}")
        raise InvalidClassroomCode("Invalid classroom code")
