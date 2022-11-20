from aiogram.dispatcher.filters.state import State, StatesGroup


class ReportStates(StatesGroup):
    input_message = State()
    none = State()