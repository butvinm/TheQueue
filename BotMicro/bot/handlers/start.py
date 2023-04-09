from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.callbacks.menu import MenuOpenCallback

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.delete()
    await message.answer(
        text='Hi!',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Menu',
                    callback_data=MenuOpenCallback().pack()
                )
            ]
        ])
    )
