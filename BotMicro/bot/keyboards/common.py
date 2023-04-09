from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.menu import MenuOpenCallback
from bot.callbacks.queue_page import QueuePageOpenCallback


def OpenMenuKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            )
        ]
    ])


def MenuAndQueueKeyboard(queue_name: str, queue_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            ),
            InlineKeyboardButton(
                text=f'Go to {queue_name}',
                callback_data=QueuePageOpenCallback(queue_key=queue_key).pack()
            )
        ]
    ])
