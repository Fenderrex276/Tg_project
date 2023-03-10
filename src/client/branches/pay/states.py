from aiogram.dispatcher.filters.state import State, StatesGroup


class PayStates(StatesGroup):

    input_sum = State()
    none = State()
    first_m = State()
    second_m = State()
    third_m = State()
    fourth_m = State()