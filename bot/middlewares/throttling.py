from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled

from loader import _, config
from services.user import permanent_ban


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = config.RATE_LIMIT, key_prefix: str = 'antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict[str]):
        await self._throttle(message, data)

    async def on_process_callback_query(self, query: CallbackQuery, data: dict[str]):
        await self._throttle(query.message, data)

    async def _throttle(self, message: Message, data: dict[str]):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')
        else:
            limit = self.rate_limit
            key = f'{self.prefix}_message'
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as throttled:

            user = data['user']

            if user.is_admin:
                return

            if throttled.exceeded_count == 3:
                await message.reply(_('Прекрати спамить!'))
            if throttled.exceeded_count == 4:
                await message.reply(_('Я тебя сейчас забаню!'))
            if throttled.exceeded_count == 5:
                if user.banned_until > datetime.now():
                    await message.reply(_('Добро пожаловать в перманентный бан. ГГВП. Сайонара'))
                    permanent_ban(user.id)

                if user.ban_count == 1:
                    await message.reply(_('Я тебя забанил, пока только на три часа. С каждым разом будет все больше'))
                else:
                    await message.reply(_('Бан на {hours}').format(
                        hours=user.banned_until - datetime.now()))

            raise CancelHandler()
