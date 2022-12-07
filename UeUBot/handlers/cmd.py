from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from callbacks import OpenMenuCallback
from messages_manager import MessagesManager
from queues import get_queues, update_queues


def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command(commands=['start']))
    dp.message.register(change_name, Command(commands=['rename']))


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
    await MessagesManager.clear_chat(message.chat.id)
    args = message.text.replace('/rename ', '').split('-')
    if len(args) != 2:
        await message.answer(
            'Incorrect format, try: /rename "old name"-"new name"'
        )
    
    old_name = args[0].strip().strip('"')
    new_name = args[1].strip().strip('"')

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
