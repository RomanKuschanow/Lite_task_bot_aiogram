from datetime import datetime

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from loader import _
from services.user import get_or_create_user


class UsersMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: dict[str]):
        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()

        from_user = message.from_user

        user = data['user'] = get_or_create_user(from_user)

        if user.is_banned:
            raise CancelHandler()

        if user.banned_until and user.banned_until > datetime.now():
            await message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=user.banned_until - datetime.now()))
            raise CancelHandler()

        await message.answer_chat_action('typing')

    @staticmethod
    async def on_process_callback_query(callback_query: CallbackQuery, data: dict[str]):
        from_user = callback_query.from_user

        user = data['user'] = get_or_create_user(from_user)

        if user.is_banned:
            raise CancelHandler()

        if user.banned_until and user.banned_until > datetime.now():
            await callback_query.message.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=user.banned_until - datetime.now()))
            raise CancelHandler()

    @staticmethod
    async def on_process_inline_query(inline_query: InlineQuery, data: dict[str]):
        from_user = inline_query.from_user

        user = data['user'] = get_or_create_user(from_user)

        if user.is_banned:
            raise CancelHandler()

        if user.banned_until and user.banned_until > datetime.now():
            await inline_query.answer(_('Чел, ты в <s>муте</s> бане еще на {date}').format(
                date=user.banned_until - datetime.now()))
            raise CancelHandler()
