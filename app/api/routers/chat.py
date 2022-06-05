import uuid

from aioredis.client import Redis
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.managers import ConnectionManager
from app.db import create_cache
from app.db.schemas import Message

router = APIRouter(
    prefix='/api', tags=['api'], dependencies=[Depends(ConnectionManager)]
)

manager = ConnectionManager()


@router.get('/messages')
async def fetch_messages(
    redis: Redis = Depends(create_cache),
) -> list[Message]:
    messages = await redis.lrange('chat', 0, -1)
    messages = [Message(content=mes) for mes in messages]

    return messages


@router.post('/threads')
async def create_thread():
    thread_id = uuid.uuid4()
    return {'thread_id': thread_id}


@router.websocket('/ws/{thread_id}')
async def websocket_endpoint(
    websocket: WebSocket, thread_id: str, redis: Redis = Depends(create_cache)
) -> None:
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, exp=websocket)

            await redis.publish('chat', f'#{thread_id}: {data}')
            await redis.rpush('chat', f'#{thread_id}: {data}')
            await redis.ltrim('chat', 0, 49)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await redis.publish('chat', f'#{thread_id}: left the chat')
