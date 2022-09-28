import asyncio
import os

from aiogram import Bot, Dispatcher

from utils.json_manager import JsonManager

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

sm = JsonManager()
loop = asyncio.get_event_loop()
loop.run_until_complete(sm.connect('./storages/queues.json'))
