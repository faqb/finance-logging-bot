from aiogram.dispatcher.filters.state import State, StatesGroup


class LangState(StatesGroup):
    change = State()

