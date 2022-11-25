from aiogram.dispatcher.filters.state import State, StatesGroup


class ReviewStates(StatesGroup):
    input_review = State()
    input_pass_review = State()
    archive = State()
    none = State()