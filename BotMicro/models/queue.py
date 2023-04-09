from odetam.async_model import AsyncDetaModel
from pydantic import Field


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
