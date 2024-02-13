import logging

from classroom import Classroom
from session import Session
from user import User

class InvalidCredentials(Exception):
    pass

class EmailAlreadyUsed(Exception):
    pass

class Controller():
    def __init__(self) -> None:
        self.__sessions_controller: Session = Session()
        self.__users: list[User] = []
        self.__classrooms: list[Classroom] = []

    def register(self, name: str, email: str, password: str) -> str:
        logging.info(f"Registering user with email: {email}")
        for user in self.__users:
            if user.email == email:
                logging.info(f"Email: {email} is already in use")
                raise EmailAlreadyUsed("Email is already in use")
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
        raise InvalidCredentials("Email or password is incorrect")
    
    def get_user(self, token: str) -> User:
        return self.__sessions_controller.get_user(token)
    
    def check_token(self, token: str) -> bool:
        return self.__sessions_controller.check_token(token)
