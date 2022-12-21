import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from config import Config
from messages_manager import MessagesManager
from routers import register_handlers


def main():
    Config.update_config()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    TelegramMethod.emit = MessagesManager.register_emit(TelegramMethod.emit)

    bot = Bot(Config.TOKEN)

    dp = Dispatcher()
    dp.message.middleware.register(MessagesManager.middleware)

    register_handlers(dp)
    
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
