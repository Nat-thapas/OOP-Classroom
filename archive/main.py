import logging

from datetime import datetime
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
from classroom import Classroom, Item
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


@app.get("/verify", tags=["Authentication"])
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


@app.post("/create-classroom", tags=["Classroom"])
async def create_classroom(classroomInfo: ClassroomInfo):
    token: str = classroomInfo.token
    name: str = classroomInfo.name
    section: str | None = classroomInfo.section
    subject: str | None = classroomInfo.subject
    room: str | None = classroomInfo.room
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    classroom_id: str = controller.create_classroom(user, name, section, subject, room)
    return {"status": "success", "classroom_id": classroom_id}


@app.post("/join-classroom", tags=["Classroom"])
async def join_classroom(classroomCode: ClassroomCode):
    token: str = classroomCode.token
    code: str = classroomCode.code
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom_id = controller.join_classroom(user, code)
        return {"status": "success", "classroom_id": classroom_id}
    except InvalidClassroomCode:
        raise InvalidClassroomCodeHTTPException
    except AlreadyInClassroom:
        raise AlreadyInClassroomHTTPException
    

@app.get("/classrooms", tags=["Classroom"])
async def classrooms(token: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    classrooms: list[Classroom] = controller.get_classrooms_for_user(user)
    return {"status": "success", "classrooms_data": [classroom.short_dict(user) for classroom in classrooms]}


@app.get("/classroom/{id}", tags=["Classroom"])
async def get_classroom(token: str, id: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(id)
        return {"status": "success", "classroom_data": classroom.long_dict(user)}
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotInClassroomHTTPException
    
@app.get("/user/{id}", tags=["User"])
async def get_user(token: str, id: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    try:
        user: User = controller.get_user(id)
        return {"status": "success", "user_data": user.dict()}
    except LookupError:
        raise UserNotFoundHTTPException
    
@app.post("/classroom/{classroom_id}/material", tags=["Classroom"])
async def add_material(classroom_id: str, material: ClassMaterial):
    token: str = material.token
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(classroom_id)
        if classroom.owner != user:
            raise PermissionError("User is not owner of classroom")
        try:
            topic = classroom.get_topic(material.topic_id) if material.topic_id else None
            assigned_to: list[User] | None
            if material.assigned_to:
                assigned_to = []
                for user_id in material.assigned_to:
                    try:
                        assigned_to.append(controller.get_user(user_id))
                    except Exception:
                        pass
            else:
                assigned_to = None
            # TODO: Add attachment
            item_id: str = classroom.add_material(topic, None, assigned_to, material.title, material.description).id
            return {"status": "success", "item_id": item_id}
        except LookupError:
            raise ItemNotFoundHTTPException
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotClassroomOwnerHTTPException
    
@app.post("/classroom/{classroom_id}/announcement", tags=["Classroom"])
async def add_announcement(classroom_id: str, announcement: ClassAnnouncement):
    token: str = announcement.token
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(classroom_id)
        if classroom.owner != user:
            raise PermissionError("User is not owner of classroom")
        try:
            topic = classroom.get_topic(announcement.topic_id) if announcement.topic_id else None
            assigned_to: list[User] | None
            if announcement.assigned_to:
                assigned_to = []
                for user_id in announcement.assigned_to:
                    try:
                        assigned_to.append(controller.get_user(user_id))
                    except Exception:
                        pass
            else:
                assigned_to = None
            # TODO: Add attachment
            item_id: str = classroom.add_announcement(topic, None, assigned_to, announcement.announcement_text).id
            return {"status": "success", "item_id": item_id}
        except LookupError:
            raise ItemNotFoundHTTPException
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotClassroomOwnerHTTPException
    
@app.post("/classroom/{classroom_id}/assignment", tags=["Classroom"])
async def add_assignment(classroom_id: str, assignment: ClassAssignment):
    token: str = assignment.token
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(classroom_id)
        if classroom.owner != user:
            raise PermissionError("User is not owner of classroom")
        try:
            topic = classroom.get_topic(assignment.topic_id) if assignment.topic_id else None
            rubric = classroom.get_rubric(assignment.rubric_id) if assignment.rubric_id else None
            assigned_to: list[User] | None
            if assignment.assigned_to:
                assigned_to = []
                for user_id in assignment.assigned_to:
                    try:
                        assigned_to.append(controller.get_user(user_id))
                    except Exception:
                        pass
            else:
                assigned_to = None
            due_date: datetime | None = datetime.fromtimestamp(assignment.due_date) if assignment.due_date else None
            # TODO: Add attachment
            item_id: str = classroom.add_assignment(topic, None, assigned_to, assignment.title, assignment.instruction, due_date, assignment.point, rubric).id
            return {"status": "success", "item_id": item_id}
        except LookupError:
            raise ItemNotFoundHTTPException
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotClassroomOwnerHTTPException
    
@app.post("/classroom/{classroom_id}/question", tags=["Classroom"])
async def add_question(classroom_id: str, question: ClassQuestion):
    token: str = question.token
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(classroom_id)
        if classroom.owner != user:
            raise PermissionError("User is not owner of classroom")
        try:
            topic = classroom.get_topic(question.topic_id) if question.topic_id else None
            assigned_to: list[User] | None
            # TODO: Move convert logic to controller
            if question.assigned_to:
                assigned_to = []
                for user_id in question.assigned_to:
                    try:
                        assigned_to.append(controller.get_user(user_id))
                    except Exception:
                        pass
            else:
                assigned_to = None
            due_date: datetime | None = datetime.fromtimestamp(question.due_date) if question.due_date else None
            # TODO: Add attachment
            item_id: str = classroom.add_question(topic, None, assigned_to, question.question_text, question.instruction, due_date, question.point).id
            return {"status": "success", "item_id": item_id}
        except LookupError:
            raise ItemNotFoundHTTPException
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotClassroomOwnerHTTPException
    
@app.get("/classroom/{classroom_id}/items", tags=["Classroom"])
async def get_items(token: str, classroom_id: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(classroom_id)
        if not classroom.verify_user(user):
            raise PermissionError("User not in classroom")
        return {"status": "success", "items_data": [item.dict() for item in classroom.items]}
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotInClassroomHTTPException
    
@app.get("/classroom/{classroom_id}/item/{item_id}", tags=["Classroom"])
async def get_item(token: str, classroom_id: str, item_id: str):
    if not controller.check_token(token):
        raise InvalidTokenHTTPException
    user: User = controller.get_user_from_token(token)
    try:
        classroom: Classroom = controller.get_classroom(classroom_id)
        if not classroom.verify_user(user):
            raise PermissionError("User not in classroom")
        try:
            item: Item = classroom.get_item(item_id)
            return {"status": "success", "item_data": item.dict()}
        except LookupError:
            raise ItemNotFoundHTTPException
    except LookupError:
        raise ClassroomNotFoundHTTPException
    except PermissionError:
        raise NotInClassroomHTTPException
