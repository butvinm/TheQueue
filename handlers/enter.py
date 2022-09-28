from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['enter'])
async def enter(message: Message):
    args = message.text.split()
    if len(args) == 1:
        await message.answer(
            'You forgot set queue name.\n'
            'Try send command like "/enter@queue2421_bot <QueueName>"'
        )
    else:
        queue_name = ' '.join(args[1:])
        result = sm.add_to_queue(queue_name, message.from_user.full_name)

        if result >= 0:
            await message.answer(f'You now at "{queue_name}" at position {result}')
        elif result == -1:
            await message.answer(
                f'Queue "{queue_name}" does not exist\n' 
                'Call /list@queue2421_bot to watch it'
            )
        elif result == -2:
            await message.answer(
                f'User already in {queue_name}.\n' 
                'Call /list@queue2421_bot to watch it'
            )