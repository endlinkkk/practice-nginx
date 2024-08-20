from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi import UploadFile
from punq import Container

from main.app.application.adapters.files.files import FastAPIFileAdapter
from main.app.application.api.files.schemas import SFile
from main.app.init import init_container
from main.app.services.files.files import UploadFileService


router = APIRouter(tags=['Files'])


@router.get("/files", status_code=status.HTTP_200_OK, description="Get all files")
def get_files_handler() -> list[SFile]: ...


@router.post("/files", status_code=status.HTTP_201_CREATED, description="Upload File")
def post_files_handler(file: UploadFile, container: Container = Depends(init_container)):
    file_service: UploadFileService = container.resolve(UploadFileService)
    file_service.save_file(FastAPIFileAdapter(file))
    return status.HTTP_201_CREATED


@router.get(
    "/files/{file_name}",
    status_code=status.HTTP_200_OK,
    description="Get File By Filename",
)
def get_file_by_filename_handler(file_name: str) -> SFile: ...
