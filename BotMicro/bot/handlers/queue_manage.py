from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.queue_manage import (CursorDownCallback, CursorUpCallback,
                                        DeleteQueueCallback, GoDownCallback,
                                        GoUpCallback, LeaveQueueCallback)
from bot.handlers.queue_page import queue_page_open_handler
from bot.keyboards.common import kb_from_btns
from bot.keyboards.menu import open_menu_btns
from bot.utils.init_message import edit_init_message
from models.queue import Queue

router = Router()


@router.callback_query(GoUpCallback.filter())
async def go_up_callback_handler(query: CallbackQuery, message: Message, callback_data: GoUpCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_existed_or_none(callback_data.queue_key)
    if not queue:
        await edit_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    user_position = queue.members.index(query.from_user.id)
    user_position = user_position - 1 if user_position > 0 else len(queue.members) - 1
    queue.members.remove(query.from_user.id)
    queue.members.insert(user_position, query.from_user.id)
    await queue.save()  # type: ignore

    await queue_page_open_handler(query, message, callback_data, bot, state)


@router.callback_query(GoDownCallback.filter())
async def go_down_callback_handler(query: CallbackQuery, message: Message, callback_data: GoDownCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_existed_or_none(callback_data.queue_key)
    if not queue:
        await edit_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    user_position = queue.members.index(query.from_user.id)
    user_position = user_position + 1 if user_position < len(queue.members) - 1 else 0
    queue.members.remove(query.from_user.id)
    queue.members.insert(user_position, query.from_user.id)
    await queue.save()  # type: ignore

    await queue_page_open_handler(query, message, callback_data, bot, state)


@router.callback_query(CursorUpCallback.filter())
async def cursor_up_callback_handler(query: CallbackQuery, message: Message, callback_data: CursorUpCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_existed_or_none(callback_data.queue_key)
    if not queue:
        await edit_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    queue.cursor = queue.cursor - 1 if queue.cursor > 0 else len(queue.members) - 1
    await queue.save()  # type: ignore

    await queue_page_open_handler(query, message, callback_data, bot, state)


@router.callback_query(CursorDownCallback.filter())
async def cursor_down_callback_handler(query: CallbackQuery, message: Message, callback_data: CursorDownCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_existed_or_none(callback_data.queue_key)
    if not queue:
        await edit_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    queue.cursor = queue.cursor + 1 if queue.cursor < len(queue.members) - 1 else 0
    await queue.save()  # type: ignore

    await queue_page_open_handler(query, message, callback_data, bot, state)


@router.callback_query(LeaveQueueCallback.filter())
async def leave_queue_callback_handler(query: CallbackQuery, message: Message, callback_data: LeaveQueueCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_existed_or_none(callback_data.queue_key)
    if not queue:
        await edit_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    queue.members.remove(query.from_user.id)
    await queue.save()  # type: ignore

    await edit_init_message(
        message, bot, state,
        text='You left the queue',
        reply_markup=kb_from_btns(open_menu_btns())
    )


@router.callback_query(DeleteQueueCallback.filter())
async def delete_queue_callback_handler(query: CallbackQuery, message: Message, callback_data: DeleteQueueCallback, bot: Bot, state: FSMContext):
    queue = await Queue.get_existed_or_none(callback_data.queue_key)
    if not queue:
        await edit_init_message(
            message, bot, state,
            text='Queue not found',
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    await queue.delete()  # type: ignore

    await edit_init_message(
        message, bot, state,
        text='Queue deleted',
        reply_markup=kb_from_btns(open_menu_btns())
    )
