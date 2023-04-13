from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.my_queues import MyQueuesCallback
from bot.keyboards.common import kb_from_btns
from bot.keyboards.menu import open_menu_btns
from bot.keyboards.queues_list import queues_list_btns
from bot.utils.init_message import edit_init_message
from models.queue import Queue

router = Router()


@router.callback_query(MyQueuesCallback.filter())
async def my_queues_handler(query: CallbackQuery, message: Message, callback_data: MyQueuesCallback, bot: Bot, state: FSMContext):
    queues = await Queue.query(Queue.deleted == False)  # type: ignore
    queues = [queue for queue in queues if (queue.creator == message.chat.id) or (message.chat.id in queue.members)]

    await edit_init_message(
        message, bot, state,
        text='Your membered or owned queues:',
        reply_markup=kb_from_btns(queues_list_btns(queues), open_menu_btns())
    )
