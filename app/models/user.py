from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UpdateUserModel(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=64)]
    email: EmailStr
    old_password: Annotated[str, Field(min_length=8, max_length=64)]
    new_password: Annotated[str, Field(min_length=8, max_length=64)] | None
