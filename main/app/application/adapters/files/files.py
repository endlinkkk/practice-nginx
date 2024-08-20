from fastapi import UploadFile
from dataclasses import dataclass
from main.app.application.adapters.files.base import IFile


@dataclass
class FastAPIFileAdapter(IFile):
    upload_file: UploadFile

    def read(self) -> bytes:
        return self.upload_file.file.read()

    def filename(self) -> str:
        return self.upload_file.filename