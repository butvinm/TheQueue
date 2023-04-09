from aiogram.fsm.state import State, StatesGroup


class NewQueueStates(StatesGroup):
    name = State()
