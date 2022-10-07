import logging

import dotenv
from aiogram import executor

import handlers
import bot


dotenv.load_dotenv('./.env')
logging.basicConfig(level=logging.INFO)

executor.start_polling(bot.dp)
