from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import chat


def create_api() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware, allow_origins=['http://localhost', 'http://localhost:3000']
    )
    app.include_router(chat.router)

    return app
