import logging

from aiogram import Dispatcher
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from callbacks import (OpenMenuCallback, OpenQueueCallback, QueueDownCallback,
                       QueueNextCallback, QueuePrevCallback, QueueUpCallback,
                       UpdateQueueCallback)
from messages_manager import MessagesManager
from queues import Queue, get_queue, update_queue


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(
        open_queue_handler,
        OpenQueueCallback.filter()
    )
    dp.callback_query.register(
        update_queue_handler,
        UpdateQueueCallback.filter()
    )
    dp.callback_query.register(
        prev_handler,
        QueuePrevCallback.filter()
    )
    dp.callback_query.register(
        next_handler,
        QueueNextCallback.filter()
    )
    dp.callback_query.register(
        down_handler,
        QueueDownCallback.filter()
    )
    dp.callback_query.register(
        up_handler,
        QueueUpCallback.filter()
    )


async def open_queue_handler(query: CallbackQuery):
    await query.answer()

    logging.info(f'Open Queue: {query.data}')

    if query.message is not None:
        chat_id = query.message.chat.id
        await MessagesManager.clear_chat(chat_id)

        queue_name = OpenQueueCallback.unpack(query.data or '').queue_name
        queue = get_queue(queue_name)
        if not queue:
            return

        await query.message.answer(
            queue.name,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text='Update',
                    callback_data=UpdateQueueCallback(
                        queue_name=queue.name).pack()
                )
            ]])
        )

        await query.message.answer(
            text=get_members_list(queue),
            reply_markup=get_queue_menu_kb(queue.name)
        )


async def update_queue_handler(query: CallbackQuery):
    await query.answer()

    logging.info(f'Update Queue: {query.data}')

    if query.message is not None:
        chat_id = query.message.chat.id
        chat_msgs = MessagesManager.get_chat_messages(chat_id)
        if not chat_msgs:
            return

        msg = chat_msgs[-1]

        queue_name = UpdateQueueCallback.unpack(query.data or '').queue_name
        queue = get_queue(queue_name)
        if not queue:
            return

        await msg.edit_text(text=get_members_list(queue), reply_markup=get_queue_menu_kb(queue.name))


async def prev_handler(query: CallbackQuery):
    await query.answer()

    logging.info(f'Prev Queue: {query.data}')

    if query.message is not None:
        queue_name = QueuePrevCallback.unpack(query.data or '').queue_name
        queue = get_queue(queue_name)
        if not queue:
            return

        if queue.pointer > 0:
            queue.pointer -= 1

        update_queue(queue)

        chat_id = query.message.chat.id
        chat_msgs = MessagesManager.get_chat_messages(chat_id)
        if not chat_msgs:
            return

        msg = chat_msgs[-1]
        await msg.edit_text(text=get_members_list(queue), reply_markup=get_queue_menu_kb(queue.name))


async def next_handler(query: CallbackQuery):
    await query.answer()

    logging.info(f'Next Queue: {query.data}')

    if query.message is not None:
        queue_name = QueueNextCallback.unpack(query.data or '').queue_name
        queue = get_queue(queue_name)
        if not queue:
            return

        if queue.pointer < len(queue.members) - 1:
            queue.pointer += 1

        update_queue(queue)

        chat_id = query.message.chat.id
        chat_msgs = MessagesManager.get_chat_messages(chat_id)
        if not chat_msgs:
            return

        msg = chat_msgs[-1]
        await msg.edit_text(text=get_members_list(queue), reply_markup=get_queue_menu_kb(queue.name))


async def up_handler(query: CallbackQuery):
    logging.info(f'Up Queue: {query.data}')

    if query.message is None:
        return

    queue_name = QueueUpCallback.unpack(query.data or '').queue_name
    queue = get_queue(queue_name)
    if not queue:
        return

    username = query.from_user.full_name
    if not username in queue.members:
        return await query.answer(f'Not such user: {username}')

    await query.answer()
    user_pos = queue.members.index(username)
    if user_pos < 1:
        return

    queue.members.pop(user_pos)
    queue.members.insert(user_pos - 1, username)
    update_queue(queue)

    chat_id = query.message.chat.id
    chat_msgs = MessagesManager.get_chat_messages(chat_id)
    if not chat_msgs:
        return

    msg = chat_msgs[-1]
    await msg.edit_text(text=get_members_list(queue), reply_markup=get_queue_menu_kb(queue.name))


async def down_handler(query: CallbackQuery):
    logging.info(f'Down Queue: {query.data}')

    if query.message is None:
        return

    queue_name = QueueDownCallback.unpack(query.data or '').queue_name
    queue = get_queue(queue_name)
    if not queue:
        return
    
    username = query.from_user.full_name
    if not username in queue.members:
        return await query.answer(f'Not such user: {username}')

    await query.answer()

    user_pos = queue.members.index(username)
    if user_pos >= len(queue.members) - 1:
        return 

    queue.members.pop(user_pos)
    queue.members.insert(user_pos + 1, username)
    update_queue(queue)

    chat_id = query.message.chat.id
    chat_msgs = MessagesManager.get_chat_messages(chat_id)
    if not chat_msgs:
        return

    msg = chat_msgs[-1]
    await msg.edit_text(text=get_members_list(queue), reply_markup=get_queue_menu_kb(queue.name))


def get_members_list(queue: Queue) -> str:
    members_list = ''
    for i, m in enumerate(queue.members):
        if i < queue.pointer:
            marker = '⚫'
        elif i == queue.pointer:
            marker = '⚪'
        elif i - queue.pointer <= 3:
            marker = '🟢'
        elif i - queue.pointer <= 6:
            marker = '🟡'
        elif i - queue.pointer <= 9:
            marker = '🟠'
        else:
            marker = '🔴'

        members_list += f'{marker} {m}\n'

    return members_list


def get_queue_menu_kb(queue_name: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='🔙 Previous', callback_data=QueuePrevCallback(queue_name=queue_name).pack()
            ),
            InlineKeyboardButton(
                text='Next 🔜', callback_data=QueueNextCallback(queue_name=queue_name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='⬇️ Down Me', callback_data=QueueDownCallback(queue_name=queue_name).pack()
            ),
            InlineKeyboardButton(
                text='Up Me ⬆️', callback_data=QueueUpCallback(queue_name=queue_name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Bact to Menu',
                callback_data=OpenMenuCallback().pack()
            )
        ]
    ])

    return markup
