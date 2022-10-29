from aiogram.dispatcher.filters.state import State, StatesGroup


class Promo(StatesGroup):
    input_promo = State()
    geo_position = State()
    none = State()
