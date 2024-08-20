from abc import ABC
from dataclasses import dataclass

from main.app.application.adapters.files.base import IFile
from main.app.repositories.files.base import BaseFileRepository


@dataclass
class BaseFileService(ABC):
    _repository: BaseFileRepository
    file: IFile
