from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.menu import MenuOpenCallback
from bot.keyboards.common import kb_from_btns
from bot.keyboards.menu import menu_btns
from bot.states.common import CommonStates
from bot.utils.init_message import edit_init_message

router = Router()


@router.callback_query(MenuOpenCallback.filter())
async def open_menu_handler(query: CallbackQuery, message: Message, callback_data: MenuOpenCallback, bot: Bot, state: FSMContext):
    await edit_init_message(
        message, bot, state,
        text='Available functions:',
        reply_markup=kb_from_btns(menu_btns())
    )
    await state.set_state(CommonStates.none)
