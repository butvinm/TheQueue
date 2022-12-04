from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Chat(DataClassJsonMixin):
    messages: list[int]


@dataclass
class Messages(DataClassJsonMixin):
    chats: dict[int, Chat]
