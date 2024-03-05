from .classroom import Classroom
from .user import User


class Controller:
    def __init__(self) -> None:
        self.__users: list[User] = []
        self.__classrooms: list[Classroom] = []

    def add_user(self, user: User) -> bool:
        if user in self.__users:
            return False
        self.__users.append(user)
        return True

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

    def add_classroom(self, classroom: Classroom) -> bool:
        if classroom in self.__classrooms:
            return False
        self.__classrooms.append(classroom)
        return True

controller = Controller()
