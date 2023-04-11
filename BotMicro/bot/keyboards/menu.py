from aiogram.types import InlineKeyboardButton

from bot.callbacks.enroll_queue import EnrollQueueStartCallback
from bot.callbacks.menu import MenuOpenCallback
from bot.callbacks.my_queues import MyQueuesCallback
from bot.callbacks.new_queue import NewQueueStartCallback


def open_menu_btns():
    return [
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            )
        ]
    ]


def menu_btns():
    return [
        [
            InlineKeyboardButton(
                text='New queue',
                callback_data=NewQueueStartCallback().pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='My queues',
                callback_data=MyQueuesCallback().pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Enroll queue',
                callback_data=EnrollQueueStartCallback().pack()
            )
        ]
    ]
