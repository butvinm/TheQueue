from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.common import OpenMenuKeyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    await message.answer(
        text='Hi!',
        reply_markup=OpenMenuKeyboard()
    )
