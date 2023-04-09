from aiogram.fsm.state import State, StatesGroup


class EnrollQueueStates(StatesGroup):
    enroll_key = State()
    wait_confirm = State()
