from aiogram.types import InlineKeyboardButton

from bot.callbacks.queue_page import QueuePageOpenCallback
from models.queue import Queue


def queues_list_btns(queues: list[Queue]):
    return [
        [
            InlineKeyboardButton(
                text=queue.name,
                callback_data=QueuePageOpenCallback(queue_key=queue.queue_key).pack()
            )
        ]
        for queue in queues
    ]
