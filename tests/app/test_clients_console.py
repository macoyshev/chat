import pytest

from app.clients import console


@pytest.mark.asyncio
async def test_load_messages(capsys, mock_aioconsole, mock_aiohttp_get):
    mock_aioconsole.ainput.return_value = 'y'
    mock_aiohttp_get.return_value.__aenter__.return_value.json.return_value = [
        {'content': 'test'}
    ]

    await console.load_previous_messages()
    captured = capsys.readouterr()

    assert captured.out == 'test\n'


@pytest.mark.asyncio
async def test_cancel_load_messages(mock_aioconsole):
    mock_aioconsole.ainput.return_value = 'n'

    res = await console.load_previous_messages()

    assert res is None


@pytest.mark.asyncio
async def test_listen_channel(capsys, mock_aioredis_pubsub):
    await console.listen_channel()
    captured = capsys.readouterr()

    assert captured.out == 'test\n'
    mock_aioredis_pubsub.assert_called_once()
