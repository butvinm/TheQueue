from abc import ABC, abstractmethod
from typing import Any

from aiogram import Router
from aiogram.types.base import TelegramObject


class BasePage(ABC):
    name: str
    router: Router

    @abstractmethod
    async def open(self, event: TelegramObject) -> Any:
        pass
