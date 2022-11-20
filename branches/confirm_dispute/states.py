from aiogram.dispatcher.filters.state import State, StatesGroup


class Promo(StatesGroup):
    choose_dispute = State()
    input_promo = State()
    geo_position = State()
    none = State()
