from pydantic import BaseModel, EmailStr


class RegisterModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordModel(BaseModel):
    old_password: str
    new_password: str
