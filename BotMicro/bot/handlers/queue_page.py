from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from bot.callbacks.queue_page import QueuePageOpenCallback
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

    await message.edit_text(
        text=f'Queue: {queue.name}',
        reply_markup=OpenMenuKeyboard()
    )
