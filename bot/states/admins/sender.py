from aiogram.dispatcher.filters.state import StatesGroup, State


class Sender(StatesGroup):
    text_all = State()
    id = State()
    text_private = State()
