from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi import UploadFile
from punq import Container

from main.app.application.adapters.files.files import FastAPIFileAdapter
from main.app.application.api.files.schemas import SFileInfo
from main.app.init import init_container
from main.app.services.files.files import FileService
from main.app.services.files.utils import (
    create_a_record_of_the_file_status,
    read_file_status,
)


router = APIRouter(tags=["Files"])


@router.get("/files", status_code=status.HTTP_200_OK, description="Get all files")
def get_files_handler() -> list[SFileInfo]:
    return read_file_status()


@router.post("/upload", status_code=status.HTTP_201_CREATED, description="Upload file")
def post_files_handler(
    file: UploadFile, container: Container = Depends(init_container)
):
    file_service: FileService = container.resolve(FileService)
    file_service.save_file(FastAPIFileAdapter(file))
    return status.HTTP_201_CREATED


@router.post(
    "/file_status",
    status_code=status.HTTP_201_CREATED,
    description="Makes  record of safe files and viruses",
)
def post_file_status_handler(file_info: SFileInfo):
    create_a_record_of_the_file_status(file_info.filename, file_info.status)



