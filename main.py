import logging
import os

# fix bag with \r character at linux system
os.environ = {key: value.strip() for key, value in os.environ.items()}
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    # yea, inner imports is stupid,
    # by I need to make some monkey patching before running

    from aiogram import executor

    from bot import bot, dp
    from handlers import *

    executor.start_polling(dp)
