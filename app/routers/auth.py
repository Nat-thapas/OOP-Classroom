from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..dependencies.dependencies import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from ..exceptions.user import EmailAlreadyInUse
from ..internal.controller import controller
from ..models.auth import LoginModel, RegisterModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
async def register(body: RegisterModel):
    try:
        user = controller.create_user(
            body.username, body.email, get_password_hash(body.password)
        )
    except EmailAlreadyInUse as exp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use"
        ) from exp

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully."},
        headers={"Authorization": create_access_token(data={"id": user.id})},
    )


@router.post("/login")
async def login(body: LoginModel):
    user = authenticate_user(body.email, body.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User logged in successfully."},
        headers={"Authorization": create_access_token(data={"id": user.id})},
    )
