from aiogram.types import Message
from bot import dp
from json_utils import add_queue


@dp.message_handler(commands=['add'])
async def add(message: Message):
    args = message.text.split()
    if len(args) == 1:
        await message.answer(
            'You forgot set queue name.\n'
            'Try send command like "/add@queue2421_bot <QueueName>"'
        )
    else:
        queue_name = ' '.join(args[1:])
        result = add_queue(queue_name)
        
        if result:
            await message.answer(f'Queue "{queue_name}" successful created')
        else:
            await message.answer(
                f'Queue "{queue_name}" already exists.\n' 
                'Call /list@queue2421_bot to watch it'
            )
