import json
from typing import Any, Optional, Union

from aiofiles import open

from utils.storage_manager import StorageManager


class JsonManager(StorageManager):
    """Manager of JSON queues storage
    JSON scheme:
    {
        "Queue1": {"pos": 0, "users": ["Alex", "Peter", ...]},
        ...
    }

    pos - position of cursor at queue user list
    users - list of queues members

    """

    def __init__(self) -> None:
        self.queues: dict[str, Any] = {}

    async def connect(self, storage_path: str):
        """Connect to json file by path

        Args:
            storage_path (str): Path to json file

        """
        self._storage = await open(storage_path, 'r+')
        self.data = await self._read()

    async def add_queue(self, queue_name: str) -> int:
        if queue_name in self.data:
            return 0

        self.data[queue_name] = {"cur": 0, "users": []}
        await self._write(self.data)

        return 1

    async def remove_queue(self, queue_name: str) -> int:
        if queue_name not in self.data:
            return 0

        self.data.pop(queue_name)
        await self._write(self.data)

        return 1

    async def add_to_queue(self, queue_name: str, full_name: str) -> int:
        if queue_name not in self.data:
            return -1

        if full_name in self.data[queue_name]['users']:
            return -2

        cur = self.data[queue_name]['cur']
        self.data[queue_name]['users'].append(full_name)
        await self._write(self.data)

        return len(self.data[queue_name]['users'])

    async def remove_from_queue(self, queue_name: str, full_name: str) -> int:
        if queue_name not in self.data:
            return -1

        if full_name not in self.data[queue_name]['users']:
            return -2

        user_index = self.data[queue_name]['users'].index(full_name)
        if user_index <= self.data[queue_name]['cur'] and user_index:
            self.data[queue_name]['cur'] -= 1

        self.data[queue_name]['users'].remove(full_name)
        await self._write(self.data)

        return len(self.data[queue_name]['users'])

    async def get_queue(self, queue_name: str) -> Optional[dict[str, Any]]:
        return self.data.get(queue_name, None)

    async def get_queues(self) -> dict[str, dict[str, Any]]:
        return self.data

    async def get_user_in(self, queue_name: str, full_name: str) -> int:
        if queue_name not in self.data:
            return -1

        if full_name not in self.data[queue_name]['users']:
            return -2

        user_index = self.data[queue_name]['users'].index(full_name)
        cur = self.data[queue_name]['cur']
        return user_index - cur + 1 if cur <= user_index else -3

    async def get_user_in_all(self, full_name: str) -> dict[str, int]:
        result = {}
        for q_name in self.data:
            pos = await self.get_user_in(q_name, full_name)
            if pos > 0:
                result[q_name] = pos

        return result

    async def set_cursor_at(self, queue_name: str, cur_pos: int) -> Union[str, int]:
        if queue_name not in self.data:
            return -1
        
        if cur_pos > len(self.data[queue_name]['users']) or cur_pos < 1:
            return -2
        
        cur_pos -= 1
        self.data[queue_name]['cur'] = cur_pos
        return self.data[queue_name]['users'][cur_pos]

    async def offset_cursor(self, queue_name: str) -> str:
        if queue_name not in self.data:
            return -1
        
        cur_pos = self.data[queue_name]['cur']
        cur_pos += 1
        if cur_pos == len(self.data[queue_name]['users']):
            cur_pos = 0
        
        self.data[queue_name]['cur'] = cur_pos
        return self.data[queue_name]['users'][cur_pos]

    async def _read(self) -> dict[str, Any]:
        """Read and return self.data from json file"""

        await self._storage.seek(0)
        json_content = await self._storage.read()
        self.data = json.loads(json_content)
        return self.data

    async def _write(self, data: dict[str, Any]) -> dict:
        """Write self.data to json file"""

        self.data = data
        json_content = json.dumps(self.data)
        await self._storage.seek(0)
        await self._storage.truncate()
        await self._storage.write(json_content)
        await self._storage.flush()

    async def __del__(self):
        """Close storage file"""

        self._write(self.self.data)
        self._storage.close()
