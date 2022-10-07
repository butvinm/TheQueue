from aiogram.types import Message
from bot import dp, bot, sm

@dp.message_handler(commands=['start'])
async def start(message: Message):
    text = 'Available commands:\n'
    
    commands = await bot.get_my_commands()
    for command in commands:
        text += f'/{command.command} - {command.description}\n'
    
    await message.answer(text)
