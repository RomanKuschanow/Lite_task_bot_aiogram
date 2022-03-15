from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from services.user import get_or_create_user


class UsersMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: dict):
        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()

        await message.answer_chat_action('typing')

        session = data['session'] = message.bot.get('session')
        user = data['user'] = await get_or_create_user(session, message.from_user)

    @staticmethod
    async def on_pre_process_callback_query(callback_query: CallbackQuery, data: dict):
        from_user = callback_query.from_user

        session = data['session'] = callback_query.bot.get('session')
        user = data['user'] = await get_or_create_user(session, from_user)
