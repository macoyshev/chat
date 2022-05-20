from fastapi import FastAPI

from .routers import chat


def create_api() -> FastAPI:
    app = FastAPI()

    app.include_router(chat.router)

    return app
