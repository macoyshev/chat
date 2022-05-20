import asyncio

import aioconsole
import aiohttp
from websockets.client import connect as ws_connect
from websockets.legacy.client import WebSocketClientProtocol

from app.configs import Endpoints
from app.db import create_cache


async def listen_to_console(socket: WebSocketClientProtocol) -> None:
    while True:
        await socket.send(await aioconsole.ainput())


async def load_previous_messages() -> None:
    res = await aioconsole.ainput('Load last 50 messages?[y/n]:')
    if res != 'y':
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(Endpoints().fetch_messages) as resp:
            messages = await resp.json()

        for mes in messages:
            print(mes['content'])


async def listen_channel() -> None:
    redis = await create_cache()
    pub_sub = redis.pubsub()
    await pub_sub.subscribe('chat')

    async for res in pub_sub.listen():
        if res['type'] == 'message':
            print(res['data'].decode())


async def main() -> None:
    nickname = await aioconsole.ainput('Choose your nickname: ')
    websocket_endpoint = Endpoints().websocket.format(nickname)

    await load_previous_messages()

    async with ws_connect(websocket_endpoint) as websocket:
        await asyncio.gather(listen_channel(), listen_to_console(websocket))


if __name__ == '__main__':
    asyncio.run(main())
