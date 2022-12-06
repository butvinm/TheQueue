from functools import partial

from aiogram import Dispatcher, Router, F
from aiogram.types.base import TelegramObject
from base_page import BasePage


class PageViewer:
    def __init__(self, dp: Dispatcher) -> None:
        self.router = Router(name='PageViewer')
        dp.include_router(self.router)

    def register_page(self, page: BasePage):
        self.router.include_router(page.router)
        self.router.callback_query.register(
            partial(self.open_page, page),
            page.open_callback.filter(),
        )

    # TODO:
    # change page opening logic

    async def open_page(self, page: BasePage, event: TelegramObject):
        
        print(event)
        await page.open(event)