from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.callbacks.enroll_queue import (EnrollQueueConfirmCallback,
                                        EnrollQueueStartCallback)
from bot.callbacks.menu import MenuOpenCallback
from bot.keyboards.common import MenuAndQueueKeyboard, OpenMenuKeyboard
from bot.states.enroll_queue import EnrollQueueStates
from models.queue import Queue

router = Router()


@router.callback_query(EnrollQueueStartCallback.filter())
async def enroll_queue_start_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.edit_text(
        text='Enter queue enroll key:',
        reply_markup=OpenMenuKeyboard()
    )

    await state.set_state(EnrollQueueStates.enroll_key)
    await state.update_data(init_message_id=message.message_id)


@router.message(EnrollQueueStates.enroll_key)
async def enroll_key_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    data = await state.get_data()

    if not message.text:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['init_message_id'],
            text='Invalid enroll key. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    queue = await Queue.get_or_none(key=message.text)
    if queue is None:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['init_message_id'],
            text='Queue not found. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
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


@router.callback_query(EnrollQueueConfirmCallback.filter(), EnrollQueueStates.wait_confirm)
async def confirm_enroll_handler(query: CallbackQuery, message: Message, state: FSMContext):
    data = await state.get_data()

    queue = await Queue.get_or_none(key=data['queue_key'])
    if queue is None:
        await message.edit_text(
            text='Queue not found. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    queue.members.append((message.from_user.id, message.from_user.full_name))
    await queue.save()  # type: ignore

    await message.edit_text(
        text=f'Queue enrolled: {queue.name}',
        reply_markup=MenuAndQueueKeyboard(queue.name, queue.key)
    )
    await state.clear()
