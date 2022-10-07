from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['move'])
async def move(message: Message):
    args = message.text.split()
    if len(args) <= 2:
        await message.answer(
            'You forgot set queue name or cursor position.\n'
            'Try send command like "/move@queue2421_bot <QueueName> <pos>"'
        )
    else:
        queue_name, pos = ' '.join(args[1:-1]), args[-1]
        try:
            pos = int(pos)
        except ValueError:
            await message.answer(f'Position must be integer but "{pos}" taken')
            return

        result = await sm.move(queue_name, pos, message.from_user.full_name)
        
        if result == -1:
            await message.answer(f'Queue "{queue_name}" does not exists')
        elif result == -2:
            await message.answer(f'Position out of boundary')
        elif result == -3:
            await message.answer(f'User not in "{queue_name}".\n')
        else:
            await message.answer(f'You now at "{queue_name}" at position {result}')