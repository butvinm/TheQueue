from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['set'])
async def set(message: Message):
    args = message.text.split()
    if len(args) <= 2:
        await message.answer(
            'You forgot set queue name or cursor position.\n'
            'Try send command like "/set@queue2421_bot <QueueName> <pos>"'
        )
    else:
        queue_name, cur_pos = ' '.join(args[1:-1]), args[-1]
        try:
            cur_pos = int(cur_pos)
        except ValueError:
            await message.answer(f'Cursor position must be integer but {cur_pos} taken')
            return

        result = await sm.set_cursor_at(queue_name, cur_pos)
        
        if result == -1:
            await message.answer(f'Queue "{queue_name}" does not exists')
        elif result == -2:
            await message.answer(f'Cursor position out of boundary')
        else:
            await message.answer(f'Next in {queue_name} is {result}')