from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.queue_page import QueuePageOpenCallback
from bot.keyboards.common import kb_from_btns
from bot.keyboards.menu import open_menu_btns
from bot.keyboards.queue_page import queue_creator_btns, queue_member_btns
from bot.utils.init_message import edit_init_message
from models.queue import Queue

router = Router()


@router.callback_query(QueuePageOpenCallback.filter())
async def queue_page_open_handler(query: CallbackQuery, message: Message, callback_data: QueuePageOpenCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_or_none(callback_data.queue_key)
    if queue is None:
        await edit_init_message(
            message, bot, state,
            text='Queue not found.',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    text = f'Queue: <b>{queue.name}</b>\n'
    if queue.creator == message.chat.id:
        text += f'Enroll key: <code>{queue.queue_key}</code>\n'
        text += f'Enroll link: <code>https://t.me/ueueueueueue_bot?start={queue.queue_key}</code>\n\n'

    text += build_queue_list(queue)

    btns = [queue_member_btns(queue.queue_key)]
    if queue.creator == message.chat.id:
        btns.append(queue_creator_btns(queue.queue_key))

    await edit_init_message(
        message, bot, state,
        text=text,
        reply_markup=kb_from_btns(*btns)
    )


def build_queue_list(queue: Queue):
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
