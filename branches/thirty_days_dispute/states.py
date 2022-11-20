from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesDispute(StatesGroup):
    account = State()
    knowledge_base = State()
    change_name = State()
    none = State()
    video_note = State()
    video = State()
    new_question = State()
    diary = State()
