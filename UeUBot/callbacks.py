from aiogram.filters.callback_data import CallbackData


class OpenMenuCallback(CallbackData, prefix='menu.open'):
    pass


class UpdateMenuCallback(CallbackData, prefix='menu.update'):
    pass


class OpenQueueCallback(CallbackData, prefix='queue.open'):
    queue_name: str


class UpdateQueueCallback(CallbackData, prefix='queue.update'):
    queue_name: str


class QueuePrevCallback(CallbackData, prefix='queue.prev'):
    queue_name: str


class QueueNextCallback(CallbackData, prefix='queue.next'):
    queue_name: str


class QueueUpCallback(CallbackData, prefix='queue.up'):
    queue_name: str


class QueueDownCallback(CallbackData, prefix='queue.down'):
    queue_name: str
