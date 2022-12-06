from abc import ABC, abstractmethod
from typing import Any

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types.base import TelegramObject


class PageOpenCallback(CallbackData, prefix='page.open'):
    name: str


class BasePage(ABC):
    name: str
    router: Router

    def __init__(self) -> None:
        super().__init__()

        self.open_callback = PageOpenCallback(name=self.name)
        
    @abstractmethod
    async def open(self, event: TelegramObject) -> Any:
        pass
