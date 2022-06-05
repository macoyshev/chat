from aioredis.client import Redis
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.managers import ConnectionManager
from app.db import create_cache
from app.db.schemas import Message

router = APIRouter(
    prefix='/chat', tags=['chat'], dependencies=[Depends(ConnectionManager)]
)

manager = ConnectionManager()


@router.get('/messages')
async def fetch_messages(
    redis: Redis = Depends(create_cache),
) -> list[Message]:
    messages = await redis.lrange('chat', 0, -1)
    messages = [Message(content=mes) for mes in messages]

    return messages


@router.websocket('/ws/{username}')
async def websocket_endpoint(
    websocket: WebSocket, username: str, redis: Redis = Depends(create_cache)
) -> None:
    await manager.connect(websocket)
    await redis.publish('chat', f'#{username}: joined to the chat')
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
            await redis.publish('chat', f'#{username}: {data}')
            await redis.rpush('chat', f'#{username}: {data}')
            await redis.ltrim('chat', 0, 49)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await redis.publish('chat', f'#{username}: left the chat')
