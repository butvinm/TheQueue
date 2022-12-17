from typing import Any, Awaitable, Callable, Coroutine, TypeVar

from aiogram import Bot
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram.types.base import TelegramObject


class IncomingMiddleware(BaseMiddleware):
    def __init__(self, handler: Callable[[TelegramObject], Any]) -> None:
        super().__init__()
        self.handler = handler

    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        self.handler(event)
        return await handler(event, data)


T = TypeVar('T')


class MessagesManager:
    messages: dict[int, list[Message]] = {}
    _middleware: IncomingMiddleware

    @classmethod
    async def clear_chat(cls, chat_id: int):
        chat_msgs = cls.messages.get(chat_id, [])
        while chat_msgs:
            try:
                await chat_msgs.pop().delete()
            except:
                pass
    
    @classmethod
    def get_chat_messages(cls, chat_id: int) -> list[Message]:
        return cls.messages.get(chat_id, [])

    @classmethod
    @property
    def middleware(cls) -> IncomingMiddleware:
        if not hasattr(MessagesManager, '_middleware'):
            cls._middleware = IncomingMiddleware(cls.handle_event)

        return cls._middleware

    @classmethod
    def register_emit(cls, func: Callable[[TelegramMethod[T], Bot], Coroutine[Any, Any, T]]) -> Callable[[TelegramMethod[T], Bot], Coroutine[Any, Any, T]]:
        async def wrapper(self: TelegramMethod[T], bot: Bot) -> T:
            result = await func(self, bot)
            if isinstance(result, TelegramObject):
                cls.handle_event(result)

            return result

        return wrapper

    @classmethod
    def handle_event(cls, event: TelegramObject) -> None:
        if isinstance(event, Message):
            chat_id = event.chat.id
            cls.messages.setdefault(chat_id, []).append(event)
