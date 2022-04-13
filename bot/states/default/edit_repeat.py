from aiogram.dispatcher.filters.state import State, StatesGroup


class EditRepeat(StatesGroup):
    count = State()
    until = State()
    range = State()
