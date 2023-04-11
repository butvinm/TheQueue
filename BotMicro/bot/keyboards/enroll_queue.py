from aiogram.types import InlineKeyboardButton

from bot.callbacks.enroll_queue import EnrollQueueConfirmCallback
from bot.callbacks.menu import MenuOpenCallback


def confirm_enroll_btns(queue_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Confirm',
                callback_data=EnrollQueueConfirmCallback(queue_key=queue_key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Cancel',
                callback_data=MenuOpenCallback().pack()
            )
        ]
    ]
