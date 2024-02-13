import logging

import os
import time
from dataclasses import dataclass
from uuid import uuid4

from dotenv import load_dotenv

from user import User

load_dotenv()

TOKEN_VALID_TIME: float = float(os.getenv("TOKEN_VALID_TIME", "86400"))


@dataclass
class TokenData:
    user: User
    time_created: float
    vaild_until: float


class ExpiredToken(Exception):
    pass

class InvalidToken(Exception):
    pass


class Session:
    def __init__(self) -> None:
        self.__tokens: dict[str, TokenData] = {}

    def check_token(self, token: str) -> bool:
        if token not in self.__tokens:
            logging.info(f"Token: {token} was searched, but does not exist")
            return False
        token_data: TokenData = self.__tokens[token]
        if time.time() > token_data.vaild_until:
            return False
        return True

    def add_user(self, user: User) -> str:
        token: str = str(uuid4())
        logging.info(f"Adding user: {user.name} with token: {token} to session")
        self.__tokens[token] = TokenData(
            user, time.time(), time.time() + TOKEN_VALID_TIME
        )
        return token

    def get_user(self, token: str) -> User:
        if token not in self.__tokens:
            logging.info(f"Token: {token} was searched, but does not exist")
            raise InvalidToken
        token_data: TokenData = self.__tokens[token]
        if time.time() > token_data.vaild_until:
            raise ExpiredToken("Token expired")
        return token_data.user
