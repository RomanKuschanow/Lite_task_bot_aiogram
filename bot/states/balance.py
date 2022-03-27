from aiogram.dispatcher.filters.state import StatesGroup, State


class Balance(StatesGroup):
    top_up_balance = State()
