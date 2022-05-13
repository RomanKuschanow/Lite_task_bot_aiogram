from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from services.user import get_user


class Status(BoundFilter):
    key = 'status'

    def __init__(self, status: str):
        self.status = status

    async def check(self, message: Message):
        user = get_user(message.from_user.id)

        if not user:
            return False

        return user.status == self.status
