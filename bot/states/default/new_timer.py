from aiogram.dispatcher.filters.state import State, StatesGroup


class NewTimer(StatesGroup):
    time = State()
    text = State()
