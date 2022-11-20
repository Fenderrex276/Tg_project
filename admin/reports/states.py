from aiogram.dispatcher.filters.state import State, StatesGroup


class ReportStates(StatesGroup):
    input_message = State()
    none = State()
    input_id_dispute = State()
    input_number_day = State()
