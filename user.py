from __future__ import annotations

import logging

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

password_hasher = PasswordHasher()


class User:
    def __init__(self, name: str, email: str, password: str) -> None:
        self.__name: str = name
        self.__email: str = email
        self.__hashed_password: str = password_hasher.hash(password)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    def check_password(self, password: str) -> bool:
        try:
            password_hasher.verify(self.__hashed_password, password)
        except (VerificationError, VerifyMismatchError):
            logging.info(f"Password verification failure for user: {self.__name}")
            return False
        if password_hasher.check_needs_rehash(self.__hashed_password):
            logging.info(f"Re-hashing password for user: {self.__name}")
            self.__hashed_password = password_hasher.hash(password)
        return True
