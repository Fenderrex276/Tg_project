from aiogram.dispatcher.filters.state import State, StatesGroup


class ReviewStates(StatesGroup):
    input_review = State()
    none = State()