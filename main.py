import logging

from fastapi import FastAPI, HTTPException, status

from controller import Controller, InvalidCredentials, EmailAlreadyInUse
from user import User
from http_exceptions import *

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
    return {"status": "success", "message": f"You're {user.name}"}


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
