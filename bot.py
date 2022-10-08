import asyncio
import os
from datetime import datetime
from typing import Any, Awaitable, Callable

import aiofiles
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from utils.json_manager import JsonManager


class LoggingMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.log_file = None

    async def connect_file(self):
        self.log_file = await aiofiles.open(os.environ['LOG_PATH'], 'a')

    async def on_pre_process_message(self, message: Message, data: dict):
        await self._log(message)
    
    async def _log(self, message: Message):
        if self.log_file is None:
            await self.connect_file()

        time = datetime.now()
        username = message.from_user.username
        msg = message.text

        log = f'[{time:%d/%m/%Y %H:%M:%S}][{username}] {msg}\n'
        await self.log_file.write(log)
        await self.log_file.flush()


bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

storage_path = os.environ['STORAGES_PATH']
json_storage_path = os.path.join(storage_path, 'queues.json')

sm = JsonManager()
loop = asyncio.get_event_loop()
loop.run_until_complete(sm.connect(json_storage_path))
