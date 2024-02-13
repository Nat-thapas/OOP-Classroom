import logging

from fastapi import FastAPI

from controller import (
    Controller,
    EmailAlreadyInUse,
    InvalidClassroomCode,
    InvalidCredentials,
)
from http_exceptions import *
from user import User
from classroom import Classroom

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)

app = FastAPI()

controller = Controller()


@app.get("/")
async def home(token: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    classrooms: list[Classroom] = controller.get_classrooms_for_user(user)
    return {"status": "success", "classrooms_id": [classroom.id for classroom in classrooms]}


@app.post("/register")
async def register(name: str, email: str, password: str):
    try:
        token: str = controller.register(name, email, password)
        return {"status": "success", "token": token}
    except EmailAlreadyInUse:
        raise EmailAlreadyInUseHTTPException


@app.post("/login")
async def login(email: str, password: str):
    try:
        token: str = controller.login(email, password)
        return {"status": "success", "token": token}
    except InvalidCredentials:
        raise InvalidCredentialsHTTPException


@app.post("/create-classroom")
async def create_classroom(
    token: str, name: str, section: str | None, subject: str | None, room: str | None
):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    classroom_id: str = controller.create_classroom(user, name, section, subject, room)
    return {"status": "success", "classroom_id": classroom_id}


@app.post("/join-classroom")
async def join_classroom(token: str, code: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    try:
        classroom_id = controller.join_classroom(user, code)
        return {"status": "success", "classroom_id": classroom_id}
    except InvalidClassroomCode:
        raise InvalidClassroomCodeHTTPException


@app.get("/classroom/{id}")
async def get_classroom(token: str, id: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    try:
        classroom: Classroom = controller.get_classroom(id)
        return {"status": "success", "classroom_data": classroom.get_dict_repr(user)}
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotInClassroomHTTPException
