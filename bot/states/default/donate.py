from aiogram.dispatcher.filters.state import StatesGroup, State


class Donate(StatesGroup):
    top_up_balance = State()
