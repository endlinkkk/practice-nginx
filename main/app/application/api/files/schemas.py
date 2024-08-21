from pydantic import BaseModel
from enum import Enum


class fileStatusEnum(str, Enum):
    clean = "clean"
    infected = "infected"


class SFile(BaseModel):
    title: str
    size: int


class SFileInfo(BaseModel):
    filename: str
    status: str
