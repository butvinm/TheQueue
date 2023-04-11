from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.callbacks.enroll_queue import (EnrollQueueConfirmCallback,
                                        EnrollQueueStartCallback)
from bot.callbacks.menu import MenuOpenCallback
from bot.keyboards.common import MenuAndQueueKeyboard, OpenMenuKeyboard
from bot.states.common import CommonStates
from bot.states.enroll_queue import EnrollQueueStates
from bot.utils.init_message import edit_init_message
from models.queue import Queue

router = Router()


@router.callback_query(EnrollQueueStartCallback.filter())
async def enroll_queue_start_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await edit_init_message(
        message, bot, state,
        text='Enter queue enroll key:',
        reply_markup=OpenMenuKeyboard()
    )

    await state.set_state(EnrollQueueStates.enroll_key)


@router.message(EnrollQueueStates.enroll_key)
async def enroll_key_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    if not message.text:
        await edit_init_message(
            message, bot, state,
            text='Invalid enroll key. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    queue = await Queue.get_or_none(key=message.text)
    if queue is None:
        await edit_init_message(
            message, bot, state,
            text='Queue not found. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    await edit_init_message(
        message, bot, state,
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
async def confirm_enroll_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    queue = await Queue.get_or_none(key=data['queue_key'])
    if queue is None:
        await edit_init_message(
            message, bot, state,
            text='Queue not found. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    chat_id, full_name = message.chat.id, message.chat.full_name
    if not chat_id in queue.members:
        queue.members.append(chat_id)

    # always update name to have relevant one
    queue.members_names[chat_id] = full_name
    await queue.save()  # type: ignore

    await edit_init_message(
        message, bot, state,
        text=f'Queue enrolled: {queue.name}',
        reply_markup=MenuAndQueueKeyboard(queue.name, queue.key)
    )
    await state.set_state(CommonStates.none)
