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
        session = message.bot.get('session')
        checked_user = await get_user(session, message.from_user.id)
        humanize.i18n.activate(checked_user.language)
        if not (checked_user.banned_until == None or checked_user.banned_until < datetime.now()):
            await message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(checked_user.banned_until - datetime.now(), minimum_unit='minutes',
                                           format='%0.0f')))
            raise CancelHandler()

        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()

        await message.answer_chat_action('typing')

        session = data['session'] = message.bot.get('session')
        user = data['user'] = await get_or_create_user(session, message.from_user)

    @staticmethod
    async def on_pre_process_callback_query(callback_query: CallbackQuery, data: dict):
        session = callback_query.bot.get('session')
        checked_user = await get_user(session, callback_query.from_user.id)
        humanize.i18n.activate(checked_user.language)
        if not (checked_user.banned_until == None or checked_user.banned_until.replace(
                tzinfo=None) < datetime.now().replace(tzinfo=None)):
            await callback_query.message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(
                    checked_user.banned_until.replace(tzinfo=None) - datetime.now().replace(tzinfo=None),
                    minimum_unit='minutes',
                    format='%0.0f')))
            raise CancelHandler()

        from_user = callback_query.from_user

        session = data['session'] = callback_query.bot.get('session')
        user = data['user'] = await get_or_create_user(session, from_user)
