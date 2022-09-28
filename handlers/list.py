from aiogram.types import Message
from bot import dp, sm


@dp.message_handler(commands=['list'])
async def list(message: Message):
    args = message.text.split()
    if len(args) == 1:
        queues = await sm.get_queues()
        if queues:
            for q_name, q_members  in queues.items():
                await display_queue(message, q_name, q_members)
        else:
            await message.answer('No existing queues')
    else:
        queue_name = ' '.join(args[1:])
        queue_members = await sm.get_queue_members(queue_name)
        if queue_members is None:
            await message.answer(
                f'"{queue_name}" does not exist'
            )
        else:
            await display_queue(message, queue_name, queue_members)


async def display_queue(message: Message, queue_name: str, queue_members: list):
    text = f'{queue_name}:\n'
    for i, member in enumerate(queue_members):
        text += f'{i + 1}: {member}\n'
    
    await message.answer(text)