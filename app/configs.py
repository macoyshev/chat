from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379


class Endpoints(BaseSettings):
    websocket: str = 'ws://127.0.0.1:8000/ws/{}'
    fetch_messages: str = 'http://127.0.0.1:8000/chat/messages'
