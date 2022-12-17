from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesDispute(StatesGroup):
    new_timezone = State()
    account = State()
    knowledge_base = State()
    change_name = State()
    none = State()
    video_note = State()
    video = State()
    new_question = State()
    diary = State()
    promo_code = State()
    personal_goals = State()
    reports = State()
    bonuses = State()
    new_report = State()


class NewReview(StatesGroup):
    none = State()
    input_review = State()
    input_city = State()
