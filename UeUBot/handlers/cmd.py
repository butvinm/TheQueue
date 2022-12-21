import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from callbacks import OpenMenuCallback
from messages_manager import MessagesManager
from queues import get_queues, update_queues


async def start_handler(message: Message):
    await MessagesManager.clear_chat(message.chat.id)
    await message.answer(
        'Hi👋 I`m UeU Bot',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text='Go to Menu', callback_data=OpenMenuCallback().pack()
            )
        ]])
    )


async def change_name(message: Message):
    if message.from_user == None:
        return

    logging.info(f'Rename: {message.from_user.full_name}')

    await MessagesManager.clear_chat(message.chat.id)

    old_name = (message.text or '').replace('/rename', '').strip()
    if not len(old_name):
        return await message.answer(
            'Incorrect format, try:\n /rename CurrentNameInList'
        )

    new_name = message.from_user.full_name

    queues = get_queues()
    flag = False
    for queue in queues:
        if old_name in queue.members:
            queue.members[queue.members.index(old_name)] = new_name
            flag = True

    update_queues(queues)
    if flag:
        await message.answer(
            'Successfully updated'
        )
    else:
        await message.answer(
            'No matches found'
        )
