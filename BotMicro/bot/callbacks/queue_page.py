from aiogram.filters.callback_data import CallbackData


class QueuePageOpenCallback(CallbackData, prefix='queue_page.open'):
    queue_key: str
