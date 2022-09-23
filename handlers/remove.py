from aiogram.types import Message
from bot import dp
from json_utils import remove_queue


@dp.message_handler(commands=['remove'])
async def remove(message: Message):
    args = message.text.split()
    if len(args) == 1:
        await message.answer(
            'You forgot set queue name.\n'
            'Try send command like "/remove@queue2421_bot <QueueName>"'
        )
    else:
        queue_name = ' '.join(args[1:])
        result = remove_queue(queue_name)

        if result:
            await message.answer(f'Queue "{queue_name}" successful removed')
        else:
            await message.answer(
                f'Queue "{queue_name}" does not exists.\n' 
                'Call /list@queue2421_bot to watch existing queues'
            )