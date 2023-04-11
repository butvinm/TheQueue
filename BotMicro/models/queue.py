from random import choices
from string import ascii_letters, digits
from typing import Optional

from odetam.async_model import AsyncDetaModel
from pydantic import Field


def generate_key() -> str:
    return ''.join(choices(ascii_letters + digits))


class Queue(AsyncDetaModel):
    # name of queue
    name: str

    # creator user_id
    creator: int

    # members user_ids in queue order
    members: list[int] = Field(default_factory=list)

    # user_id and fullname sorted in queue order
    members_names: dict[int, str] = Field(default_factory=dict)

    # current queue position
    cursor: int = 0

    # shadow deletion
    deleted: bool = False

    @classmethod
    async def get_existed_or_none(cls, queue_key: str) -> Optional['Queue']:
        queue = await cls.get_or_none(queue_key)
        if queue and queue.deleted:
            return None

        return queue

    @property
    def queue_key(self) -> str:
        return str(self.key)
    