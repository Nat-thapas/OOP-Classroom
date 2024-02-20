from pydantic import BaseModel

class RegisterCredential(BaseModel):
    name: str
    email: str
    password: str

class LoginCredential(BaseModel):
    email: str
    password: str