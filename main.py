import logging 

logging.basicConfig(level=logging.INFO)

from aiogram import executor
from bot import bot, dp
from handlers import *


executor.start_polling(dp)