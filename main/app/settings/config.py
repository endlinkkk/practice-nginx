from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    UPLOAD_FILE_PATH: str = Field(alias="UPLOAD_FILE_PATH")


def get_settings() -> Settings:
    return Settings(_env_file=".env", _env_file_encoding="utf-8")
