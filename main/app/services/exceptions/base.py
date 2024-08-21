from dataclasses import dataclass

from main.app.domain.exceptions import ApplicationException

@dataclass(eq=False)
class ServiceException(ApplicationException):
    @property
    def message(self):
        return "there was an error processing the request"