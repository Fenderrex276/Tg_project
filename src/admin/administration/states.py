from aiogram.dispatcher.filters.state import State, StatesGroup


class AdministrationStates(StatesGroup):
    none = State()
    input_username_admin = State()
    delete_admin = State()
