from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchReminder(StatesGroup):
    text = State()
    date = State()
    time = State()
