from unittest.mock import MagicMock

import pytest
from asynctest import CoroutineMock
from fakeredis import FakeServer
from fakeredis.aioredis import FakeRedis
from fastapi.testclient import TestClient

from app.api import create_api
from app.db.schemas import Message


@pytest.fixture
def client():
    _client = TestClient(create_api())

    return _client


@pytest.fixture
def mock_aioredis(mocker):
    mocked = mocker.patch('app.db.aioredis.from_url')
    mocked.return_value = FakeRedis(server=FakeServer())
    mocked.lrange.return_value = [Message(content='test_message')]

    return mocked


async def async_magic():
    pass


@pytest.fixture
def mock_aioredis_pubsub(mocker):
    itr = MagicMock()
    itr.__aiter__.return_value = [{'type': 'message', 'data': b'test'}]

    pub_sub = MagicMock()
    pub_sub.subscribe.side_effect = CoroutineMock()
    pub_sub.listen.return_value = itr

    mocked = mocker.patch('app.db.aioredis.client.PubSub', autospec=True)
    mocked.return_value = pub_sub

    return mocked


@pytest.fixture
def mock_aioconsole(mocker):
    return mocker.patch('app.clients.console.aioconsole', autospec=True)


@pytest.fixture
def mock_websocket_protocol(mocker):
    return mocker.patch(
        'websockets.legacy.client.WebSocketClientProtocol', autospec=True
    )


@pytest.fixture
def mock_aiohttp_get(mocker):
    return mocker.patch('app.clients.console.aiohttp.ClientSession.get', autospec=True)
