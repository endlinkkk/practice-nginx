from dataclasses import dataclass

from main.app.services.exceptions.base import ServiceException

@dataclass(eq=False)
class FileNotFoundException(ServiceException):
    ...