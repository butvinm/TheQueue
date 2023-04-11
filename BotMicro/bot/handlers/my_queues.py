from typing import Iterable

from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.callbacks.menu import MenuOpenCallback
from bot.callbacks.my_queues import MyQueuesCallback
from bot.callbacks.queue_page import QueuePageOpenCallback
from bot.utils.init_message import edit_init_message
from models.queue import Queue

router = Router()


@router.callback_query(MyQueuesCallback.filter())
async def my_queues_handler(query: CallbackQuery, message: Message, callback_data: MyQueuesCallback, bot: Bot, state: FSMContext):
    queues = await Queue.get_all()
    queues = [queue for queue in queues if (queue.creator == message.chat.id) or (message.chat.id in queue.members)]

    await edit_init_message(
        message, bot, state,
        text='Your membered or owned queues:',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=build_queues_buttons(queues)
        )
    )


def build_queues_buttons(queues: Iterable[Queue]) -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=queue.name,
                callback_data=QueuePageOpenCallback(queue_key=queue.key).pack()
            )
        ]
        for queue in queues
    ] + [
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            )
        ]
    ]
