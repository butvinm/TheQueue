from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.enroll_queue import EnrollQueueConfirmCallback
from bot.callbacks.menu import MenuOpenCallback

from bot.keyboards.common import OpenMenuKeyboard
from bot.states.enroll_queue import EnrollQueueStates
from models.queue import Queue

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_link_handler(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()

    await message.delete()

    if command.args is None:
        await message.answer('Incorrect link')
        return
    
    queue = await Queue.get_or_none(command.args)
    if not queue:
        await message.answer('Queue not found')
        return
        
    await message.answer(
        text=f'Enroll to queue: {queue.name}?',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Confirm',
                    callback_data=EnrollQueueConfirmCallback(queue_key=queue.key).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='Cancel',
                    callback_data=MenuOpenCallback().pack()
                )
            ]
        ])
    )
    await state.set_state(EnrollQueueStates.wait_confirm)
    await state.update_data(queue_key=queue.key)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    await message.answer(
        text='Hi!',
        reply_markup=OpenMenuKeyboard()
    )
