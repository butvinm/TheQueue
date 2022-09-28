from aiogram import Bot, Dispatcher
import os

from utils.json_manager import JsonManager

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

sm = JsonManager()
sm.connect('./storages/queues.json')


