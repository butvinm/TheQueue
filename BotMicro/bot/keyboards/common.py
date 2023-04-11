from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def kb_from_btns(*btns: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    for btn in btns:
        buttons.extend(btn)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
