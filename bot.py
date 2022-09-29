import asyncio
import os

from aiogram import Bot, Dispatcher

from utils.json_manager import JsonManager

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

storage_path = os.environ['STORAGES_PATH']
json_storage_path = os.path.join(storage_path, 'queues.json')

sm = JsonManager()
loop = asyncio.get_event_loop()
loop.run_until_complete(sm.connect(json_storage_path))
