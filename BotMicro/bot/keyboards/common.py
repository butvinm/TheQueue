from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.menu import MenuOpenCallback


def OpenMenuKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            )
        ]
    ])
