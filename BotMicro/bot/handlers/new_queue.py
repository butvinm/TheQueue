from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.new_queue import NewQueueStartCallback
from bot.keyboards.common import kb_from_btns
from bot.keyboards.menu import open_menu_btns
from bot.states.common import CommonStates
from bot.states.new_queue import NewQueueStates
from bot.utils.init_message import edit_init_message
from models.queue import Queue

router = Router()


@router.callback_query(NewQueueStartCallback.filter())
async def new_queue_start_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await edit_init_message(
        message, bot, state,
        text='Enter queue name:',
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(NewQueueStates.name)


@router.message(NewQueueStates.name)
async def new_queue_name_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    if not message.text:
        await edit_init_message(
            message, bot, state,
            text='Incorrect name. Try again:',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    queue = Queue(name=message.text, creator=message.chat.id)  # type: ignore
    await queue.save()  # type: ignore

    await edit_init_message(
        message, bot, state,
        text=f'Queue successfully created.',
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(CommonStates.none)
