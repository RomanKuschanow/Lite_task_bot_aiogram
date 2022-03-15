from aiogram.dispatcher.filters.state import State, StatesGroup


class NewReminder(StatesGroup):
    text = State()
    date = State()
