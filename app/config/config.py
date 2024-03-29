from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="app/.env", env_file_encoding="utf-8")

    jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    classroom_code_length: int
    attachments_storage_path: Path
    banner_images_storage_path: Path
    avatar_images_storage_path: Path
    theme_colors: list[str]


@lru_cache()
def get_settings():
    return Settings()  # type: ignore
