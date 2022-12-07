import dotenv
import os


class Config:
    TOKEN: str
    QUEUES_STORAGE: str

    @classmethod
    def update_config(cls):
        dotenv.load_dotenv()  # type: ignore
        cls.TOKEN = os.environ['TOKEN']
        cls.QUEUES_STORAGE = os.environ['QUEUES_STORAGE']
