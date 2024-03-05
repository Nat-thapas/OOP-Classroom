from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    classroom_code_length: int
    file_storage_path: Path


@lru_cache()
def get_settings():
    return Settings()  # type: ignore
