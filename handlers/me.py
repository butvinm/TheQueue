from aiogram.types import Message
from bot import dp
from json_utils import get_me_at, get_me_all


@dp.message_handler(commands=['me'])
async def me(message: Message):
    full_name = message.from_user.full_name
    args = message.text.split()
    if len(args) == 1:
        poses = get_me_all(full_name)
        print(poses)
        text = f'{full_name} positions at queues:\n'
        for q_name, pos in poses.items():
            text += f'{q_name}: {pos}\n'

        await message.answer(text)

    else:
        queue_name = ' '.join(args[1:])
        pos = get_me_at(queue_name, full_name)
        if pos >= 0:
            text = f'{full_name} positions at {queue_name}: {pos}'
        else:
            text = f'{full_name} not in {queue_name}'
        
        await message.answer(text)