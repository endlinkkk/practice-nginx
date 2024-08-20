from dataclasses import dataclass

from main.app.application.adapters.files.base import IFile
from main.app.application.adapters.files.files import FastAPIFileAdapter
from main.app.repositories.files.memory import LocalFileRepository
from main.app.services.files.base import BaseFileService


@dataclass
class UploadFileService(BaseFileService):
    _repository: LocalFileRepository
    file: FastAPIFileAdapter

    def save_file(self, file: IFile):
        self._repository.add_file(file)


