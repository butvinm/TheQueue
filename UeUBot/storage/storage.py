import asyncio
from typing import Generic, Type, TypeVar

import aiofiles
from aiofiles.threadpool.binary import AsyncFileIO
from dataclasses_json import DataClassJsonMixin

T = TypeVar('T', bound=DataClassJsonMixin)


class Storage(Generic[T]):
    def __init__(self, storage_path: str, data_builder: Type[T]) -> None:
        super().__init__()

        self.storage: AsyncFileIO = asyncio.run(
            aiofiles.open(storage_path, 'r', encoding='utf-8')
        )
        self.data_builder = data_builder

    async def read(self) -> T:
        data = await self.storage.read()
        obj: T = self.data_builder.from_json(data)
        return obj

    async def write(self, obj: T) -> None:
        data = obj.to_json()
        await self.storage.write(data)
