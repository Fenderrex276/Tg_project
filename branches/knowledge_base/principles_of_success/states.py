from aiogram.dispatcher.filters.state import State, StatesGroup


class KnowledgeBaseStates(StatesGroup):
    knowledge_base = State()
    none = State()

