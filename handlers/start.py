from aiogram.types import Message
from bot import dp, sm

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(
        'User guide:\n'
        '/list - print members of all queues\n'
        '/list <Queue Name> - print members of Queue Name\n'
        '/me - print your position depend cursor in all queues\n'
        '/me <Queue Name> - print your position depend cursor in Queue Name\n'
        '/enter <Queue Name> - enter at the end of Queue Name\n'
        '/quit <Queue Name> - leave from Queue Name\n'
        '/next <Queue Name> - set queue cursor to the next member. If was at last user go to start.\n'
        '/set <Queue Name> <Cursor Position> - set cursor at specific position\n'
        '/add <QueueName> - add new empty queue with name "Queue Name"\n'
        '/start - help'
    )