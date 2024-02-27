from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import items, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"]
)


app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "Google Classroom Clone API"}