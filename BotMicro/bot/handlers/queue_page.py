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

    if queue.creator == message.chat.id:
        await show_queue_for_creator(queue, message)
    else:
        await show_queue_for_member(queue, message)


async def show_queue_for_creator(queue: Queue, message: Message):
    text = f'Queue: {queue.name}\nEnroll key: <code>{queue.key}</code>\n\n'
    text += build_queue_text(queue) 
    await message.edit_text(
        text=text,
        reply_markup=OpenMenuKeyboard()
    )


async def show_queue_for_member(queue: Queue, message: Message):
    text = f'Queue: {queue.name}\n\n'
    text += build_queue_text(queue) 
    await message.edit_text(
        text=text,
        reply_markup=OpenMenuKeyboard()
    )


def build_queue_text(queue: Queue):
    size = len(queue.members)

    text = ''
    for pos, member_data in enumerate(queue.members):
        if pos - queue.cursor < 0:
            tick = '⚫'
        elif pos - queue.cursor == 0:
            tick = '🔘'
        elif pos - queue.cursor < size // 3:
            tick = '🟢'
        elif pos - queue.cursor < size // 3 * 2:
            tick = '🟡'
        else:
            tick = '🔴'
        
        text += f'{tick} {member_data[1]}\n'
    
    return text
