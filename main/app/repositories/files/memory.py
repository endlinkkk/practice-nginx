import os
from dataclasses import dataclass
from main.app.application.adapters.files.base import IFile
from main.app.dtos.files.files import FileDTO
from main.app.repositories.files.base import BaseFileRepository

@dataclass
class LocalFileRepository(BaseFileRepository):
    
    def get_file(self, filename: str) -> FileDTO:
        file_path = os.path.join(self.path, filename)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            return FileDTO(FileDTO(title=filename, path=file_path, size=file_size))
        return None

    def add_file(self, file: IFile) -> None:
        file_path = os.path.join(self.path, file.filename())
        with open(file_path, 'wb') as f:
            f.write(file.read())