import json
from typing import Any
import pytest
from UeUBot.dataclasses import Queues, Messages


@pytest.fixture(params=(
    'tests/teststorages/queues1.json',
    'tests/teststorages/queues2.json'
))
def queues_json(request) -> dict[str, Any]:
    with open(request.param, 'r') as f:
        return json.load(f)


def test_queues_storage(queues_json: list[Any]):
    queues = Queues.from_dict(queues_json)

    assert isinstance(queues.queues, list)

    for queue, origin in zip(queues.queues, queues_json['queues']):
        assert queue.name == origin['name']
        assert queue.pointer == origin['pointer']
        assert queue.members == origin['members']



@pytest.fixture(params=(
    'tests/teststorages/messages1.json',
    'tests/teststorages/messages2.json'
))
def messages_json(request) -> dict[str, Any]:
    with open(request.param, 'r') as f:
        return json.load(f)


def test_messages_storage_correct(messages_json: list[Any]):
    messages = Messages.from_dict(messages_json)

    assert isinstance(messages.chats, dict)

    for chat, origin in zip(messages.chats, messages_json['chats']):
        assert chat.messages == origin['messages']


@pytest.fixture(params=(
    'tests/teststorages/messages3.json',
    'tests/teststorages/messages4.json'
))
def incorrect_messages_json(request) -> dict[str, Any]:
    with open(request.param, 'r') as f:
        return json.load(f)


def test_messages_storage_incorrect(incorrect_messages_json: list[Any]):
    with pytest.raises(ValueError):
        messages = Messages.from_dict(incorrect_messages_json)
