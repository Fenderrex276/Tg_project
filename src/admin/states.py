from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):
    input_key = State()
    is_admin = State()