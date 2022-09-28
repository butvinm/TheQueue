from abc import abstractmethod, ABC
from typing import Optional




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

    def remove_queue(queue_name: str) -> int:
        """Remove queue if it exists

        Args:
            queue_name (str): Name of queue to remove

        Returns:
            int: 1 if removed, 0 if does not exist 
        """

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


class StorageReader(ABC):
    """Interface for bot connection with data storage. Read-only"""

    @abstractmethod
    def connect(*args, **kwargs):
        """Connect Reader to storage (json, local/cloud database, google sheets, etc"""

    def get_queue_members(queue_name: str) -> Optional[list[str]]:
        """ See Returns

        Args:
            queue_name (str): Name of target queue

        Returns:
            Optional[list[str]]: Return list of queue members or None if queue does not exist
        """
        
    def get_queues() -> dict[str, list[str]]:
        """See Returns

        Returns:
            dict[str, list[str]]: All queues: key - Queue name, value - Queue members. 
                                Can be empty
        """

    def get_user_in(queue_name: str, full_name: str) -> int:
        """Return user positions in queue

        Args:
            queue_name (str): Target queue
            full_name (str): Telegram fullname of user

        Returns:
            int: -1 if queue not exist, -2 if not consist, else position in queue
        """

    def get_user_in_all(full_name: str) -> dict[str, int]:
        """Return user positions in all queues where him consists

        Args:
            full_name (str): Telegram fullname of user

        Returns:
            dict[str, int]: User positions in queues: key - Queue name, value - position
        """


class StorageManager(StorageReader, StorageWriter):
    """Interface for bot connection with data storage. Both write and read access"""