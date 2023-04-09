from odetam.async_model import AsyncDetaModel
from pydantic import Field


class Queue(AsyncDetaModel):
    # name of queue
    name: str

    # creator user_id
    creator: int

    # list of user_id and fullname sorted in queue order
    members: list[tuple[int, str]] = Field(default_factory=list)

    # current queue position
    cursor: int = 0
