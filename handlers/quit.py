from aiogram.types import Message
from bot import dp
from json_utils import remove_from_queue


@dp.message_handler(commands=['quit'])
async def quit(message: Message):
    args = message.text.split()
    if len(args) == 1:
        await message.answer(
            'You forgot set queue name.\n'
            'Try send command like "/quit@queue2421_bot <QueueName>"'
        )
    else:
        queue_name = ' '.join(args[1:])
        result = remove_from_queue(queue_name, message.chat.full_name)

        if result >= 0:
            await message.answer(f'You quit "{queue_name}", {result} people staying')
        elif result == -1:
            await message.answer(
                f'Queue "{queue_name}" does not exist.\n' 
                'Call /list@queue2421_bot to watch it'
            )
        elif result == -2:
            await message.answer(
                f'User not in "{queue_name}".\n' 
                'Call /list@queue2421_bot to watch it'
            )
