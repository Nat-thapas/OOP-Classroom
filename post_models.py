from pydantic import BaseModel

class RegisterCredential(BaseModel):
    name: str
    email: str
    password: str

class LoginCredential(BaseModel):
    email: str
    password: str

class ClassroomInfo(BaseModel):
    token: str
    name: str
    subject: str | None
    section: str | None
    room: str | None

class ClassroomCode(BaseModel):
    token: str
    code: str