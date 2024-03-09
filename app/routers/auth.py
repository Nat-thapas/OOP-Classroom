from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies.authentication import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from ..exceptions.user import EmailAlreadyInUse
from ..internal.controller import controller
from ..models.auth import RegisterModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterModel):
    try:
        user = controller.create_user(
            body.username, body.email, get_password_hash(body.password)
        )
    except EmailAlreadyInUse as exp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use"
        ) from exp
    return {
        "access_token": create_access_token(data={"id": user.id}),
        "token_type": "bearer",
    }


@router.post("/login")
async def login(body: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(body.username, body.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    token = create_access_token(data={"id": user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify_token", dependencies=[Depends(get_current_user)])
async def verify_token():
    return {"message": "You are authenticated"}
