from aiogram.filters.callback_data import CallbackData


class GoUpCallback(CallbackData, prefix='queue_page.go_up'):
    queue_key: str


class GoDownCallback(CallbackData, prefix='queue_page.go_down'):
    queue_key: str


class CursorUpCallback(CallbackData, prefix='queue_page.cursor_up'):
    queue_key: str


class CursorDownCallback(CallbackData, prefix='queue_page.cursor_down'):
    queue_key: str


class LeaveQueueCallback(CallbackData, prefix='queue_page.leave_queue'):
    queue_key: str


class DeleteQueueCallback(CallbackData, prefix='queue_page.delete_queue'):
    queue_key: str
