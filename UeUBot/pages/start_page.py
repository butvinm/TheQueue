from typing import Any

from aiogram import Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.base import TelegramObject
from aiogram.filters import Command
from base_page import BasePage, PageOpenCallback


class StartPage(BasePage):
    name = 'StartPage'
    router = Router(name=name)

    def __init__(self) -> None:
        super().__init__()

        self.router.message.register(
            self.open,
            Command(commands=['start'])
        )

    async def open(self, event: TelegramObject) -> Any:
        if isinstance(event, CallbackQuery):
            await event.answer()
            message = event.message
        elif isinstance(event, Message):
            message = event
        else:
            raise ValueError(event)

        if message:
            open_menu_kb = InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Go to menu', callback_data=PageOpenCallback(name='MenuPage').pack())
                ]]
            )
            await message.answer(
                'Hello👋 I`m UeU - bot for queues management',
                reply_markup=open_menu_kb
            )
