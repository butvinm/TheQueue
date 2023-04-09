from aiogram.filters.callback_data import CallbackData


class MyQueuesCallback(CallbackData, prefix='my_queues'):
    pass
