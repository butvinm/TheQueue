from aiogram.filters.callback_data import CallbackData


class EnrollQueueStartCallback(CallbackData, prefix='enroll_queue.start'):
    pass


class EnrollQueueConfirmCallback(CallbackData, prefix='enroll_queue.confirm'):
    queue_key: str
    