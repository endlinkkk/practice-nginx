from dataclasses import dataclass

from main.app.application.adapters.files.base import IFile
from main.app.repositories.files.memory import LocalFileRepository
from main.app.services.files.base import BaseFileService


@dataclass
class FileService(BaseFileService):
    _repository: LocalFileRepository

    def save_file(self, file: IFile):
        self._repository.add_file(file)
