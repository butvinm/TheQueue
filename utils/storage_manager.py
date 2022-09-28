from abc import ABC, abstractmethod
from typing import Any, Optional, Union


class StorageWriter(ABC):
    """Interface for bot connection with data storage. Write-only"""

    @abstractmethod
    def connect(*args, **kwargs):
        """Connect Writer to storage (json, local/cloud database, google sheets, etc"""

    @abstractmethod
    def add_queue(queue_name: str) -> int:
        """Create new query, if it does not exist

        Args:
            queue_name (str): Name of added queue 

        Returns:
            int: 1 if new queue created, 0 if queue with same name already exists
        """

    @abstractmethod
    def remove_queue(queue_name: str) -> int:
        """Remove queue if it exists

        Args:
            queue_name (str): Name of queue to remove

        Returns:
            int: 1 if removed, 0 if does not exist 
        """

    @abstractmethod
    def add_to_queue(queue_name: str, full_name: str) -> int:
        """Add user fullname to the end of specific queue

        Args:
            queue_name (str): Name of target queue
            full_name (str): Telegram fullname of added user 

        Returns:
            int: Positive position in queue if new user added, 
                -2 if full_name already exists in queue, 
                -1 if queue does not exist
        """

    @abstractmethod
    def remove_from_queue(queue_name: str, full_name: str) -> int:
        """Remove user fullname from queue. Other users offsets by one stage

        Args:
            queue_name (str): Name of target queue
            full_name (str): Telegram fullname of removed user 

        Returns:
            int: Positive current len of queue if removed, 
                -2 if full_name does not exists, 
                -1 if queue does not exist
        """

    @abstractmethod
    def set_cursor_at(self, queue_name: str, cur_pos: int) -> Union[str, int]:
        """Set cursor position in queue at specified position

        Args:
            queue_name (str): Name of target queue
            cur_pos (int): Position of cursor

        Returns:
            Union[str, int]: -1 if queue does not exist, -2 if out of bound, else full name of current user
        """
    
    @abstractmethod
    def offset_cursor(self, queue_name: str) -> Union[str, int]:
        """Increase cursor position at one. If out of bound set to begin of queue

        Args:
            queue_name (str): Name of target queue

        Returns:
            Union[str, int]: -1 if queue does not exist, full name of current user
        """

class StorageReader(ABC):
    """Interface for bot connection with data storage. Read-only"""

    @abstractmethod
    def connect(*args, **kwargs):
        """Connect Reader to storage (json, local/cloud database, google sheets, etc"""

    @abstractmethod
    def get_queue(queue_name: str) -> Optional[dict[str, Any]]:
        """ See Returns

        Args:
            queue_name (str): Name of target queue

        Returns:
            Optional[dict[str, Any]]: Queue as {'cur': int, 'users': list[str]} or None if name does not exist
        """

    @abstractmethod
    def get_queues() -> dict[str, dict[str, Any]]:
        """See Returns

        Returns:
            list[dict[str, Any]]: Dictionary: key - queue name, value - queue as {'cur': int, 'users': list[str]}. 
                                Can be empty
        """

    @abstractmethod
    def get_user_in(queue_name: str, full_name: str) -> int:
        """Return user distance to queue cursor

        Args:
            queue_name (str): Target queue
            full_name (str): Telegram fullname of user

        Returns:
            int: -1 if queue not exist, -2 if not consist, -3 if user above cursor, else distance to cursor
        """

    @abstractmethod
    def get_user_in_all(full_name: str) -> dict[str, int]:
        """Return user distances to cursor in all queues where him consists

        Args:
            full_name (str): Telegram fullname of user

        Returns:
            dict[str, int]: User distances in queues: key - Queue name, value - distance
        """


class StorageManager(StorageReader, StorageWriter):
    """Interface for bot connection with data storage. Both write and read access"""
