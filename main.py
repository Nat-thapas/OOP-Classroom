import logging

from fastapi import FastAPI

from controller import Controller, InvalidCredentials, EmailAlreadyUsed
from user import User

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)

app = FastAPI()

controller = Controller()


@app.get("/")
async def home(token: str):
    if not controller.check_token(token):
        return {"status": "error", "exception": "InvalidToken"}
    user: User = controller.get_user(token)
    return {"status": "success", "message": f"You're {user.name}"}


@app.post("/register")
async def register(name: str, email: str, password: str):
    try:
        token: str = controller.register(name, email, password)
        return {"status": "success", "token": token}
    except EmailAlreadyUsed:
        return {"status": "error", "exception": "EmailAlreadyUsed"}


@app.post("/login")
async def login(email: str, password: str):
    try:
        token: str = controller.login(email, password)
        return {"status": "success", "token": token}
    except InvalidCredentials:
        return {"status": "error", "exception": "InvalidCredentials"}
