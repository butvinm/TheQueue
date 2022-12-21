from aiogram import Dispatcher
from aiogram.filters import Command
from callbacks import (OpenMenuCallback, OpenQueueCallback, QueueDownCallback,
                       QueueNextCallback, QueuePrevCallback, QueueUpCallback,
                       UpdateMenuCallback, UpdateQueueCallback)
from handlers.cmd import change_name, start_handler
from handlers.menu import open_menu_handler, update_menu_handler
from handlers.queue import (down_handler, next_handler, open_queue_handler,
                            prev_handler, up_handler, update_queue_handler)


def register_handlers(dp: Dispatcher):
    # Common
    dp.message.register(start_handler, Command(commands=['start']))
    dp.message.register(change_name, Command(commands=['rename']))

    # Menu Page
    dp.callback_query.register(
        open_menu_handler,
        OpenMenuCallback.filter()
    )
    dp.callback_query.register(
        update_menu_handler,
        UpdateMenuCallback.filter()
    )

    # Queue Page
    dp.callback_query.register(
        open_queue_handler,
        OpenQueueCallback.filter()
    )
    dp.callback_query.register(
        update_queue_handler,
        UpdateQueueCallback.filter()
    )
    dp.callback_query.register(
        prev_handler,
        QueuePrevCallback.filter()
    )
    dp.callback_query.register(
        next_handler,
        QueueNextCallback.filter()
    )
    dp.callback_query.register(
        down_handler,
        QueueDownCallback.filter()
    )
    dp.callback_query.register(
        up_handler,
        QueueUpCallback.filter()
    )
