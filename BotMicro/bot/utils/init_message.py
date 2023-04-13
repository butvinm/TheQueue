from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message


async def edit_init_message(
    message: Message,
    bot: Bot,
    state: FSMContext,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> Optional[Message]:
    data = await state.get_data()
    init_message_id = data.get('init_message_id')
    if init_message_id is None:
        init_message = await message.answer(
            text=text,
            reply_markup=reply_markup
        )
        await state.update_data(init_message_id=init_message.message_id)
    else:
        init_message = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=init_message_id,
            text=text,
            reply_markup=reply_markup
        )

    return init_message if isinstance(init_message, Message) else None


async def resend_init_message(
    message: Message,
    bot: Bot,
    state: FSMContext,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> Optional[Message]:
    data = await state.get_data()
    init_message_id = data.get('init_message_id')

    init_message = await message.answer(
        text=text,
        reply_markup=reply_markup
    )
    await state.update_data(init_message_id=init_message.message_id)

    if init_message_id is not None:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=init_message_id
            )
        except TelegramBadRequest:
            pass

    return init_message