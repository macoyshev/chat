from http import HTTPStatus


def test_fetch_empty_messages(client, mock_aioredis):
    res = client.get('/chat/messages')

    assert res.status_code == HTTPStatus.OK
    assert res.json() == []

    mock_aioredis.assert_called_once()


def test_fetch_messages(client, mock_aioredis):
    with client.websocket_connect('ws/test') as ws:
        ws.send_text('test_message')

    res = client.get('/chat/messages')
    messages = res.json()
    assert res.status_code == HTTPStatus.OK
    assert messages
    assert messages[0]['content'] == '#test: test_message'

    mock_aioredis.assert_called()


def test_fetch_limit_messages(client, mock_aioredis):
    with client.websocket_connect('ws/test') as ws:
        for _ in range(100):
            ws.send_text('test_message')

    res = client.get('/chat/messages')
    messages = res.json()
    assert res.status_code == HTTPStatus.OK
    assert len(messages) == 50

    mock_aioredis.assert_called()
