from dataclasses import dataclass
from typing import Any, Optional
from dataclasses_json import DataClassJsonMixin
import json
from config import Config


@dataclass
class Queue(DataClassJsonMixin):
    name: str
    pointer: int
    members: list[str]


def get_queues() -> list[Queue]:
    with open(Config.QUEUES_STORAGE, 'r', encoding='utf-8') as f:
        data: list[dict[str, Any]] = json.load(f)

    queues = [Queue.from_dict(queue_dict) for queue_dict in data]
    return queues


def get_queue(name: str) -> Optional[Queue]:
    with open(Config.QUEUES_STORAGE, 'r', encoding='utf-8') as f:
        data: list[dict[str, Any]] = json.load(f)

    for queue_dict in data:
        if queue_dict['name'] == name:
            return Queue.from_dict(queue_dict)


def update_queues(queues: list[Queue]):
    with open(Config.QUEUES_STORAGE, 'w', encoding='utf-8') as f:
        json.dump([q.to_dict() for q in queues], f)


def update_queue(queue: Queue):
    with open(Config.QUEUES_STORAGE, 'r', encoding='utf-8') as f:
        data: list[dict[str, Any]] = json.load(f)

    for i in range(len(data)):
        queue_dict = data[i]
        if queue_dict['name'] == queue.name:
            data[i] = queue.to_dict()
            break

    with open(Config.QUEUES_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(data, f)