import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from controller import (
    Controller,
    EmailAlreadyInUse,
    InvalidClassroomCode,
    InvalidCredential,
    AlreadyInClassroom,
)
from http_exceptions import *
from user import User
from classroom import Classroom
from post_models import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

controller = Controller()


@app.get("/")
async def home():
    return RedirectResponse("/docs")


@app.get("/verify")
async def verify(token: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    return {"status": "valid"}


@app.post("/register", tags=["Authentication"])
async def register(register_credential: RegisterCredential):
    name: str = register_credential.name
    email: str = register_credential.email
    password: str = register_credential.password
    try:
        token: str = controller.register(name, email, password)
        return {"status": "success", "token": token}
    except EmailAlreadyInUse:
        raise EmailAlreadyInUseHTTPException


@app.post("/login", tags=["Authentication"])
async def login(login_credential: LoginCredential):
    email: str = login_credential.email
    password: str = login_credential.password 
    try:
        token: str = controller.login(email, password)
        return {"status": "success", "token": token}
    except InvalidCredential:
        raise InvalidCredentialHTTPException


@app.post("/create-classroom", tags=["Classrooms"])
async def create_classroom(classroomInfo: ClassroomInfo):
    token: str = classroomInfo.token
    name: str = classroomInfo.name
    section: str | None = classroomInfo.section
    subject: str | None = classroomInfo.subject
    room: str | None = classroomInfo.room
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    classroom_id: str = controller.create_classroom(user, name, section, subject, room)
    return {"status": "success", "classroom_id": classroom_id}


@app.post("/join-classroom", tags=["Classrooms"])
async def join_classroom(token: str, code: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    try:
        classroom_id = controller.join_classroom(user, code)
        return {"status": "success", "classroom_id": classroom_id}
    except InvalidClassroomCode:
        raise InvalidClassroomCodeHTTPException
    except AlreadyInClassroom:
        raise AlreadyInClassroomHTTPException
    

@app.get("/classrooms", tags=["Classrooms"])
async def classrooms(token: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    classrooms: list[Classroom] = controller.get_classrooms_for_user(user)
    return {"status": "success", "classrooms_data": [classroom.short_dict(user) for classroom in classrooms]}


@app.get("/classroom/{id}", tags=["Classrooms"])
async def get_classroom(token: str, id: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user(token)
    try:
        classroom: Classroom = controller.get_classroom(id)
        return {"status": "success", "classroom_data": classroom.short_dict(user)}
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotInClassroomHTTPException
