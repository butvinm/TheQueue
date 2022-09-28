from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['next'])
async def next(message: Message):
    args = message.text.split()
    if len(args) == 1:
        await message.answer(
            'You forgot set queue name.\n'
            'Try send command like "/next@queue2421_bot <QueueName>"'
        )
    else:
        queue_name = ' '.join(args[1:])
        result = await sm.offset_cursor(queue_name)
        
        if result == -1:
            await message.answer(f'Queue "{queue_name}" does not exists')
        else:
            await message.answer(f'Next in {queue_name} is {result}')