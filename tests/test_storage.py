from random import randint
from UeUBot.dataclasses.messages import Chat
from UeUBot.storage import Storage
from UeUBot.dataclasses import Queues, Messages

import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'json_path',
    (
        'tests/teststorages/messages1.json',
        'tests/teststorages/messages2.json',
    )
)
async def test_messages_read(json_path: str):
    storage = Storage(json_path, Messages)

    messages = await storage.read()
    assert messages.chats is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'json_path',
    (
        'tests/teststorages/messages1.json',
        'tests/teststorages/messages2.json',
    )
)
async def test_message_write(json_path: str):
    storage = Storage(json_path, Messages)

    messages = await storage.read()
    messages.chats[randint(0, 100)] = Chat([123213, 12323, 12321])
    await storage.write(messages)
