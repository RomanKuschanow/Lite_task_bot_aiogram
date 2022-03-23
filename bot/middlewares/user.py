from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from loader import _
import humanize

from services.user import get_or_create_user, get_user

from datetime import datetime


class UsersMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: dict):
        await message.answer_chat_action('typing')

        session = data['session'] = message.bot.get('session')
        user = data['user'] = await get_or_create_user(session, message.from_user)

        if user.is_banned:
            raise CancelHandler()

        humanize.i18n.activate(user.language)
        if user.banned_until and user.banned_until > datetime.now():
            await message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(user.banned_until - datetime.now(), minimum_unit='minutes',
                                           format='%0.0f')))
            raise CancelHandler()

        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()


    @staticmethod
    async def on_pre_process_callback_query(callback_query: CallbackQuery, data: dict):
        from_user = callback_query.from_user

        session = data['session'] = callback_query.bot.get('session')
        user = data['user'] = await get_or_create_user(session, from_user)

        if user.is_banned:
            raise CancelHandler()

        humanize.i18n.activate(user.language)
        if user.banned_until and user.banned_until.replace(tzinfo=None) > datetime.now():
            await query.message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(
                    user.banned_until.replace(tzinfo=None) - datetime.now(),
                    minimum_unit='minutes',
                    format='%0.0f')))
            raise CancelHandler()

