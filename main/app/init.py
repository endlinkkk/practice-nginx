from functools import lru_cache
from punq import Container, Scope

from main.app.application.adapters.files.files import FastAPIFileAdapter
from main.app.repositories.files.memory import LocalFileRepository
from main.app.services.files.files import UploadFileService
from main.app.settings.config import Settings, get_settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def _init_container() -> Container:
    container = Container()

    def create_file_repository() -> LocalFileRepository:
        settings: Settings = container.resolve(Settings)
        return LocalFileRepository(path=settings.UPLOAD_FILE_PATH)
    

    def create_file_service() -> UploadFileService:
        return UploadFileService(
            _repository=container.resolve(LocalFileRepository),
        )
    
    container.register(
        service=Settings,
        factory=get_settings,
        scope=Scope.singleton
    )

    container.register(
        service=LocalFileRepository,
        factory=create_file_repository,
        scope=Scope.singleton,
    )

    container.register(
        service=UploadFileService,
        factory=create_file_service,
        scope=Scope.singleton,
    )

    return container