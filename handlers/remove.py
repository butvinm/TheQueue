from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['remove'])
async def remove(message: Message):
    if message.from_user.username != 'butvin_mihail':
        await message.answer('Sorry, you have not access to that command')
        return

    args = message.text.split()
    if len(args) == 1:
        await message.answer(
            'You forgot set queue name.\n'
            'Try send command like "/remove@queue2421_bot <QueueName>"'
        )
    else:
        queue_name = ' '.join(args[1:])
        result = await sm.remove_queue(queue_name)

        if result:
            await message.answer(f'Queue "{queue_name}" successful removed')
        else:
            await message.answer(
                f'Queue "{queue_name}" does not exists.\n' 
                'Call /list@queue2421_bot to watch existing queues'
            )
            