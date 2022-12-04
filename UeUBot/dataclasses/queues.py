from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Queue(DataClassJsonMixin):
    name: str
    pointer: int
    members: list[str]


@dataclass
class Queues(DataClassJsonMixin):
    queues: list[Queue]
