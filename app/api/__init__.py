from fastapi import FastAPI

from .routers import chat


class CORSMiddleware:
    pass


def create_api() -> FastAPI:
    app = FastAPI()

    app.add_middleware(CORSMiddleware, allow_origin_regex='*')
    app.include_router(chat.router)

    return app
