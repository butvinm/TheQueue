from aiogram import Bot


async def get_enroll_link(bot: Bot, queue_key: str) -> str:
    bot_me = await bot.me()
    return f'https://t.me/{bot_me.username}?start={queue_key}'
