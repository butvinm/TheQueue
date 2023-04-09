from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.new_queue import NewQueueStartCallback
from bot.keyboards.common import MenuAndQueueKeyboard, OpenMenuKeyboard
from bot.states.new_queue import NewQueueStates
from models.queue import Queue

router = Router()


@router.callback_query(NewQueueStartCallback.filter())
async def new_queue_start_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.edit_text(
        text='Enter queue name:',
        reply_markup=OpenMenuKeyboard()
    )

    await state.set_state(NewQueueStates.name)
    await state.update_data(init_message_id=message.message_id)


@router.message(NewQueueStates.name)
async def new_queue_name_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    data = await state.get_data()

    if not message.text:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['init_message_id'],
            text='Incorrect name. Try again:',
            reply_markup=OpenMenuKeyboard()
        )
        return

    queue = Queue(name=message.text, creator=message.chat.id)  # type: ignore
    await queue.save()  # type: ignore

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=f'Queue successfully created.',
        reply_markup=MenuAndQueueKeyboard(queue_name=queue.name, queue_key=queue.key)
    )
    await state.clear()
