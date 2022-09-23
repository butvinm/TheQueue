from aiogram import Bot, Dispatcher
import os

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)


