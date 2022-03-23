from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import Throttled

from data.config import ADMINS
from services.user import ban_user, permanent_ban, get_user
from models.base import create_async_database
from loader import _
from datetime import datetime


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=1, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        session = message.bot.get('session')
        user = await get_user(session, message.from_user.id)
        if user.is_banned:
            raise CancelHandler()

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
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def on_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        session = callback_query.bot.get('session')
        user = await get_user(session, callback_query.from_user.id)
        if user.is_banned:
            raise CancelHandler()

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
        except Throttled as t:
            await self.message_throttled(callback_query.message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        if throttled.user in ADMINS:
            return

        session = message.bot.get('session')
        user = await ban_user(session, throttled.user)
        if user.is_banned:
            raise CancelHandler()

        if throttled.exceeded_count == 3:
            await message.reply(_('Прекрати спамить!'))
        if throttled.exceeded_count == 4:
            await message.reply(_('Я тебя сейчас забаню!'))
        if throttled.exceeded_count == 5:
            if user.banned_until.replace(tzinfo=None) > datetime.now():
                await message.reply(_("Добро пожаловать в перманентный бан. ГГВП. Сайонара"))
                await permanent_ban(session, user.id)

            if user.ban_count == 1:
                await message.reply(_('Я тебя забанил, пока только на три часа. С каждым разом будет все больше'))
            else:
                import humanize
                humanize.i18n.activate(user.language)
                await message.reply(_('Бан на {hours}').format(
                    hours=humanize.precisedelta(
                        user.banned_until.replace(tzinfo=None) - datetime.now(),
                        minimum_unit='hours',
                        format='%0.0f')))
