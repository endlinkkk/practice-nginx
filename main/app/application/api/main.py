from fastapi import FastAPI
from main.app.application.api.files.handlers import router as files_router


def create_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        description='Service for working with files and checking them for viruses using nginx',
        docs_url='/api/docs',
    )
    app.include_router(router=files_router, prefix='/api')

    return app
