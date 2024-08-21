from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IFile(ABC):
    @abstractmethod
    def read(self) -> bytes:
        pass

    @abstractmethod
    def filename(self) -> str:
        pass
