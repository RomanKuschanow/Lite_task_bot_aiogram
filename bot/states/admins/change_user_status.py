from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeStatus(StatesGroup):
    user_id = State()
