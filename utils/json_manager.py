import json
from typing import Optional

from aiofiles import open

from utils.storage_manager import StorageManager


class JsonManager(StorageManager):
    def __init__(self) -> None:
        self.data = {}

    async def connect(self, storage_path: str):
        """Connect to json file by path

        Args:
            storage_path (str): Path to json file

        """
        self._storage = await open(storage_path, 'r+')

    async def add_queue(self, queue_name: str) -> int:
        data = await self._read()
        if queue_name in data:
            return False

        data[queue_name] = []
        await self._write(data)

        return True

    async def remove_queue(self, queue_name: str) -> int:
        data = await self._read()
        if queue_name not in data:
            return False

        data.pop(queue_name)
        await self._write(data)

        return True

    async def add_to_queue(self, queue_name: str, full_name: str) -> int:
        data = await self._read()
        if queue_name not in data:
            return -1

        if full_name in data[queue_name]:
            return -2

        data[queue_name].append(full_name)
        await self._write(data)

        return len(data[queue_name])

    async def remove_from_queue(self, queue_name: str, full_name: str) -> int:
        data = await self._read()
        if queue_name not in data:
            return -1

        if full_name not in data[queue_name]:
            return -2

        data[queue_name].remove(full_name)
        await self._write(data)

        return len(data[queue_name])

    async def get_queue_members(self, queue_name: str) -> Optional[list[str]]:
        data = await self._read()
        return data.get(queue_name, None)

    async def get_queues(self) -> dict[str, list[str]]:
        data = await self._read()
        return data

    async def get_user_in(self, queue_name: str, full_name: str) -> int:
        data = await self._read()
        if queue_name not in data:
            return -1

        if full_name not in data[queue_name]:
            return -2

        return data[queue_name].index(full_name) + 1

    async def get_user_in_all(self, full_name: str) -> dict[str, int]:
        data = await self._read()
        result = {}
        for q_name in data:
            pos = await self.get_user_in(q_name, full_name)
            if pos >= 0:
                result[q_name] = pos

        return result

    async def _read(self) -> dict:
        """Read and return data from json file"""

        await self._storage.seek(0)
        json_content = await self._storage.read()
        data = json.loads(json_content)
    
        return data

    async def _write(self, data) -> dict:
        """Write data to json file"""

        self.data = data
        json_content = json.dumps(data)
        await self._storage.seek(0)
        await self._storage.truncate()
        await self._storage.write(json_content)
        await self._storage.flush()

    async def __del__(self):
        self._write(self.data)
        self._storage.close()
