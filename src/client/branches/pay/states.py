from aiogram.dispatcher.filters.state import State, StatesGroup


class PayStates(StatesGroup):
    pay = State()
    input_sum = State()
    none = State()
