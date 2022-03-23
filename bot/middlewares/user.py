from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from services.user import get_or_create_user
import humanize


class UsersMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_message(message: Message, data: dict[str]):
        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()

        from_user = message.from_user

        session = data['session'] = message.bot.get('session')
        user = data['user'] = await get_or_create_user(session, from_user)

        if user.is_banned:
            raise CancelHandler()

        humanize.i18n.activate(user.language)
        if user.banned_until and user.banned_until > datetime.now():
            await message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(user.banned_until - datetime.now(), minimum_unit='minutes',
                                           format='%0.0f')))
            raise CancelHandler()

        await message.answer_chat_action('typing')

    @staticmethod
    async def on_pre_process_callback_query(callback_query: CallbackQuery, data: dict[str]):
        from_user = callback_query.from_user

        session = data['session'] = callback_query.bot.get('session')
        user = data['user'] = await get_or_create_user(session, from_user)

        if user.is_banned:
            raise CancelHandler()

        humanize.i18n.activate(user.language)
        if user.banned_until and user.banned_until > datetime.now():
            await message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(user.banned_until - datetime.now(), minimum_unit='minutes',
                                           format='%0.0f')))
            raise CancelHandler()

    @staticmethod
    async def on_pre_process_inline_query(inline_query: InlineQuery, data: dict[str]):
        from_user = inline_query.from_user

        session = data['session'] = inline_query.bot.get('session')
        user = data['user'] = await get_or_create_user(session, from_user)

        if user.is_banned:
            raise CancelHandler()

        humanize.i18n.activate(user.language)
        if user.banned_until and user.banned_until > datetime.now():
            await message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=humanize.precisedelta(user.banned_until - datetime.now(), minimum_unit='minutes',
                                           format='%0.0f')))
            raise CancelHandler()
