from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.callbacks.menu import MenuOpenCallback
from bot.callbacks.queue_page import (CursorDownCallback, CursorUpCallback,
                                      DeleteQueueCallback, GoDownCallback,
                                      GoUpCallback, LeaveQueueCallback,
                                      QueuePageOpenCallback)
from bot.keyboards.common import OpenMenuKeyboard
from models.queue import Queue

router = Router()


@router.callback_query(QueuePageOpenCallback.filter())
async def queue_page_open_handler(query: CallbackQuery, message: Message, callback_data: QueuePageOpenCallback, state: FSMContext):
    queue = await Queue.get_or_none(callback_data.queue_key)
    if queue is None:
        await message.edit_text(
            text='Queue not found.',
            reply_markup=OpenMenuKeyboard()
        )
        return

    if queue.creator == message.chat.id:
        await show_queue_for_creator(queue, message)
    else:
        await show_queue_for_member(queue, message)


async def show_queue_for_member(queue: Queue, message: Message):
    text = f'Queue: {queue.name}\n\n'
    text += build_queue_text(queue)

    await message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=build_member_buttons(queue))
    )


async def show_queue_for_creator(queue: Queue, message: Message):
    text = f'Queue: <b>{queue.name}</b>\n'
    text += f'Enroll key: <code>{queue.key}</code>\n'
    text += f'Enroll link: <code>https://t.me/ueueueueueue_bot?start={queue.key}</code>\n\n'
    text += build_queue_text(queue)
    await message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=build_member_buttons(queue) + build_creator_buttons(queue)
        )
    )


def build_queue_text(queue: Queue):
    size = len(queue.members)

    text = ''
    for pos, member_id in enumerate(queue.members):
        if pos - queue.cursor < 0:
            tick = '⚫'
        elif pos - queue.cursor == 0:
            tick = '🔘'
        elif pos - queue.cursor < size // 4:
            tick = '🟢'
        elif pos - queue.cursor < size // 4 * 2:
            tick = '🟡'
        elif pos - queue.cursor < size // 4 * 3:
            tick = '🟠'
        else:
            tick = '🔴'

        text += f'{tick} {queue.members_names[member_id]}\n'

    return text


def build_member_buttons(queue: Queue) -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text='Update',
                callback_data=QueuePageOpenCallback(queue_key=queue.key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Go Up',
                callback_data=GoUpCallback(queue_key=queue.key).pack()
            ),
            InlineKeyboardButton(
                text='Go Down',
                callback_data=GoDownCallback(queue_key=queue.key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Cursor Up',
                callback_data=CursorUpCallback(queue_key=queue.key).pack()
            ),
            InlineKeyboardButton(
                text='Cursor Down',
                callback_data=CursorDownCallback(queue_key=queue.key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Leave Queue',
                callback_data=LeaveQueueCallback(queue_key=queue.key).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Menu',
                callback_data=MenuOpenCallback().pack()
            )
        ],
    ]


def build_creator_buttons(queue: Queue) -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text='Delete',
                callback_data=DeleteQueueCallback(queue_key=queue.key).pack()
            )
        ]
    ]
