from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['list'])
async def list(message: Message):
    args = message.text.split()
    if len(args) == 1:
        queues = await sm.get_queues()
        if queues:
            for q_name, q_values in queues.items():
                q_cur, q_users = q_values.values()
                await display_queue(message, q_name, q_cur, q_users)
        else:
            await message.answer('No existing queues')
    else:
        q_name = ' '.join(args[1:])
        q_values = await sm.get_queue(q_name)
        if q_values is None:
            await message.answer(
                f'"{q_name}" does not exist'
            )
        else:
            q_cur, q_users = q_values.values()
            await display_queue(message, q_name, q_cur, q_users)


async def display_queue(message: Message, q_name: str, q_cur: int, q_users: list):
    text = f'{q_name}:\n'
    for i, member in enumerate(q_users):
        if i == q_cur:
            text += '>>'
        else:
            text += '    '
        
        text += f'{i + 1}: {member}\n'
    
    await message.answer(text)