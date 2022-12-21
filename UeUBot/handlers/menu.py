import logging

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from callbacks import OpenQueueCallback, UpdateMenuCallback
from messages_manager import MessagesManager
from queues import Queue, get_queues


async def open_menu_handler(query: CallbackQuery):
    await query.answer()

    logging.info(f'Open Menu: {query.data}')

    if query.message is not None:
        chat_id = query.message.chat.id
        await MessagesManager.clear_chat(chat_id)

        await query.message.answer(
            'Меню',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text='Update',
                    callback_data=UpdateMenuCallback().pack()
                )
            ]])
        )

        queues = get_queues()
        await query.message.answer(
            'Available queues:',
            reply_markup=get_queue_kb(queues)
        )


async def update_menu_handler(query: CallbackQuery):
    await query.answer()

    logging.info(f'Update Menu: {query.data}')

    if query.message is not None:
        chat_id = query.message.chat.id
        chat_msgs = MessagesManager.get_chat_messages(chat_id)
        if not chat_msgs:
            return

        message = chat_msgs[-1]
        queues = get_queues()
        await message.edit_reply_markup(
            reply_markup=get_queue_kb(queues)
        )


def get_queue_kb(queues: list[Queue]) -> InlineKeyboardMarkup:
    queues_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=queue.name,
            callback_data=OpenQueueCallback(queue_name=queue.name).pack()
        )] for queue in queues
    ])

    return queues_kb
