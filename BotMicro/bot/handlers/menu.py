from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.callbacks.enroll_queue import EnrollQueueStartCallback
from bot.callbacks.menu import MenuOpenCallback
from bot.callbacks.my_queues import MyQueuesCallback
from bot.callbacks.new_queue import NewQueueStartCallback

router = Router()


@router.callback_query(MenuOpenCallback.filter())
async def open_menu_handler(query: CallbackQuery, message: Message, callback_data: MenuOpenCallback, state: FSMContext):
    await state.clear()
    
    await message.edit_text(
        text='Available functions:',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
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
        ])
    )
