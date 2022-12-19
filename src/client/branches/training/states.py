from aiogram.dispatcher.filters.state import State, StatesGroup


class Video(StatesGroup):
    recv_video = State()
    recv_video_note = State()
    next_step = State()
    none = State()
    new_question = State()