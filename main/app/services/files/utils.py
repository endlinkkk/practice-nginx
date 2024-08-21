from main.app.application.api.files.schemas import SFileInfo
from main.app.services.files.converters import convert_file_status_document_to_dto

import os


def create_a_record_of_the_file_status(filename: str, status: str):
    with open("file_info.txt", "a") as f:
        f.write(f"{filename} {status}\n")


def read_file_status() -> list[SFileInfo]:
    result = []
    path = "file_info.txt"
    if os.path.isfile(path):
        with open("file_info.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                result.append(convert_file_status_document_to_dto(line))
    return result
