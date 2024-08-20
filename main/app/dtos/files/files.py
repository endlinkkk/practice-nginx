from dataclasses import dataclass



@dataclass
class FileDTO:
    title: str
    path: str
    size: int
