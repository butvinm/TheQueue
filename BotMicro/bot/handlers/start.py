from aiogram import Bot, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.common import kb_from_btns
from bot.keyboards.enroll_queue import confirm_enroll_btns
from bot.keyboards.menu import open_menu_btns
from bot.states.common import CommonStates
from bot.states.enroll_queue import EnrollQueueStates
from bot.utils.init_message import resend_init_message
from models.queue import Queue

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_link_handler(message: Message, command: CommandObject, bot: Bot, state: FSMContext):
    await message.delete()
    if command.args is None:
        await resend_init_message(
            message, bot, state,
            text='Incorrect link',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    queue = await Queue.get_existed_or_none(queue_key=command.args)
    if not queue:
        await resend_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    await resend_init_message(
        message, bot, state,
        text=f'Enroll to queue: {queue.name}?',
        reply_markup=kb_from_btns(confirm_enroll_btns(queue.queue_key))
    )
    await state.set_state(EnrollQueueStates.wait_confirm)
    await state.update_data(queue_key=queue.queue_key)


@router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    await resend_init_message(
        message, bot, state,
        text='Hi!',
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(CommonStates.none)
