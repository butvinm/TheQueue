from aiogram.types import Message
from bot import dp, sm

@dp.message_handler(commands=['me'])
async def me(message: Message):
    full_name = message.from_user.full_name
    args = message.text.split()
    if len(args) == 1:
        poses = await sm.get_user_in_all(full_name)
        text = f'{full_name} positions at queues:\n'
        print(poses)
        for q_name, pos in poses.items():
            text += f'{q_name}: {pos}\n'

        await message.answer(text)

    else:
        queue_name = ' '.join(args[1:])
        pos = await sm.get_user_in(queue_name, full_name)
        if pos >= 0:
            text = f'{full_name} positions at {queue_name}: {pos}'
        else:
            text = f'{full_name} not in {queue_name}'
        
        await message.answer(text)