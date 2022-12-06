import asyncio
from sqlite3 import connect
from typing import Generic, Optional, Type, TypeVar

import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper

from dataclasses_json import DataClassJsonMixin

T = TypeVar('T', bound=DataClassJsonMixin)


class Storage(Generic[T]):
    def __init__(self, storage_path: str, data_class: Type[T]) -> None:
        super().__init__()

        self.storage_path = storage_path
        self.data_class = data_class
        self.storage: Optional[AsyncTextIOWrapper] = None

    async def connect(self):
        if self.storage is None:
            self.storage = await aiofiles.open(self.storage_path, 'r+', encoding='utf-8')

    async def read(self) -> T:
        await self.connect()
        data = await self.storage.read()
        await self.storage.seek(0)
        obj: T = self.data_class.from_json(data)  # type: ignore
        return obj

    async def write(self, obj: T) -> None:
        await self.connect()
        data = obj.to_json()  # type: ignore
        await self.storage.write(data)
        await self.storage.truncate()