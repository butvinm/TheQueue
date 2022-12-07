import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from config import Config
from handlers import menu, queue, cmd
from messages_manager import MessagesManager


def main():
    Config.update_config()

    logging.basicConfig(level=logging.DEBUG)

    TelegramMethod.emit = MessagesManager.register_emit(TelegramMethod.emit)

    bot = Bot(Config.TOKEN)

    dp = Dispatcher()
    dp.message.middleware.register(MessagesManager.middleware)

    menu.register_handlers(dp)
    queue.register_handlers(dp)
    cmd.register_handlers(dp)

    dp.run_polling(bot)


if __name__ == '__main__':
    main()
