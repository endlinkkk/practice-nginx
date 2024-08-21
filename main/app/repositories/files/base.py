from abc import ABC, abstractmethod
from dataclasses import dataclass

from main.app.application.adapters.files.base import IFile
from main.app.domain.files.files import FileDTO

@dataclass
class BaseFileRepository(ABC):
    path: str

    @abstractmethod
    def get_file(self, filename: str) -> FileDTO:
        ...

    @abstractmethod
    def add_file(self, file: IFile):
        ...