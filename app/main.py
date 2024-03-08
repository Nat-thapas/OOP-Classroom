from contextlib import asynccontextmanager
from os import mkdir
from shutil import rmtree

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config.config import get_settings
from .routers import attachment, auth, classroom, user

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    rmtree(settings.attachments_storage_path, ignore_errors=True)
    mkdir(settings.attachments_storage_path)
    yield
    rmtree(settings.attachments_storage_path, ignore_errors=True)
    mkdir(settings.attachments_storage_path)


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)


app.include_router(auth.router)
app.include_router(attachment.router)
app.include_router(classroom.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Google Classroom Clone API"}
