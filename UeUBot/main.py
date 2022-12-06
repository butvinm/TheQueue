import logging

from aiogram import Bot, Dispatcher
from config import Config
from page_viewer import PageViewer
from pages import StartPage


def main():
    logging.basicConfig(level=logging.DEBUG)

    config = Config()

    dp = Dispatcher()
    bot = Bot(config.TOKEN, parse_mode='HTML')
 
    viewer = PageViewer(dp)
    start_page = StartPage()
    viewer.register_page(start_page)
    
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
