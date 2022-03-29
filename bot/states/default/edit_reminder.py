from aiogram.dispatcher.filters.state import State, StatesGroup


class EditReminder(StatesGroup):
    text = State()
    date = State()
    time = State()
