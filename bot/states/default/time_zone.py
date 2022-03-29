from aiogram.dispatcher.filters.state import State, StatesGroup


class TimeZone(StatesGroup):
    region = State()
    city = State()
