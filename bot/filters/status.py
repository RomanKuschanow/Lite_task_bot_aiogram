from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from services.user import get_user


class Status(BoundFilter):
    key = 'status'

    def __init__(self, status, *args, **kwargs):
        self.status = status

    async def check(self, message):
        session = message.bot.get('session')
        user = await get_user(session, message.from_user.id)

        if not user:
            return False

        return user.status == self.status
