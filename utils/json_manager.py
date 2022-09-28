import json
import logging
from typing import Optional
from utils.storage_manager import StorageManager


class JsonManager(StorageManager):
    def __init__(self) -> None:
        self.data = {}

    def connect(self, storage_path: str):
        """Connect to json file by path

        Args:
            storage_path (str): Path to json file

        """
        self._storage = open(storage_path, 'r+')

    def add_queue(self, queue_name: str) -> int:
        data = self._read()
        if queue_name in data:
            return False

        data[queue_name] = []
        self._write(data)

        return True

    def remove_queue(self, queue_name: str) -> int:
        data = self._read()
        if queue_name not in data:
            return False

        data.pop(queue_name)
        self._write(data)

        return True

    def add_to_queue(self, queue_name: str, full_name: str) -> int:
        data = self._read()
        if queue_name not in data:
            return -1

        if full_name in data[queue_name]:
            return -2

        data[queue_name].append(full_name)
        self._write(data)

        return len(data[queue_name])

    def remove_from_queue(self, queue_name: str, full_name: str) -> int:
        data = self._read()
        if queue_name not in data:
            return -1

        if full_name not in data[queue_name]:
            return -2

        data[queue_name].remove(full_name)
        self._write(data)

        return len(data[queue_name])

    def get_queue_members(self, queue_name: str) -> Optional[list[str]]:
        data = self._read()
        return data.get(queue_name, None)

    def get_queues(self) -> dict[str, list[str]]:
        data = self._read()
        return data

    def get_user_in(self, queue_name: str, full_name: str) -> int:
        data = self._read()
        if queue_name not in data:
            return -1

        if full_name not in data[queue_name]:
            return -2

        return data[queue_name].index(full_name) + 1

    def get_user_in_all(self, full_name: str) -> dict[str, int]:
        data = self._read()
        result = {}
        for q_name in data:
            pos = self.get_user_in(q_name, full_name)
            if pos >= 0:
                result[q_name] = pos

        return result

    def _read(self) -> dict:
        """Read and return data from json file"""

        self._storage.seek(0)
        try:
            data = json.load(self._storage)
        except json.JSONDecodeError:
            data = {}

        return data
    
    def _write(self, data) -> dict:
        """Write data to json file"""

        self.data = data
        self._storage.seek(0)
        self._storage.truncate()
        json.dump(data, self._storage)
    
    def __del__(self):
        self._write(self.data)
        self._storage.close()
        
