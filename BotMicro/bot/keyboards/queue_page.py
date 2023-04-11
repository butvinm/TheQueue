from aiogram.types import InlineKeyboardButton
from bot.callbacks.menu import MenuOpenCallback

from bot.callbacks.queue_manage import CursorDownCallback, CursorUpCallback, DeleteQueueCallback, GoDownCallback, GoUpCallback, LeaveQueueCallback
from bot.callbacks.queue_page import QueuePageOpenCallback


def open_queue_btns(queue_name: str, queue_key: str):
    return [
        [
            InlineKeyboardButton(
                text=f'Go to "{queue_name}"',
                callback_data=QueuePageOpenCallback(queue_key=queue_key).pack()
            )
        ]
    ]


def queue_member_btns(queue_key: str) -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text='Update',
                callback_data=QueuePageOpenCallback(queue_key=queue_key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Go Up',
                callback_data=GoUpCallback(queue_key=queue_key).pack()
            ),
            InlineKeyboardButton(
                text='Go Down',
                callback_data=GoDownCallback(queue_key=queue_key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Cursor Up',
                callback_data=CursorUpCallback(queue_key=queue_key).pack()
            ),
            InlineKeyboardButton(
                text='Cursor Down',
                callback_data=CursorDownCallback(queue_key=queue_key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Leave Queue',
                callback_data=LeaveQueueCallback(queue_key=queue_key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            )
        ],
    ]


def queue_creator_btns(queue_key: str) -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text='Delete ⚠️',
                callback_data=DeleteQueueCallback(queue_key=queue_key).pack()
            )
        ]
    ]
