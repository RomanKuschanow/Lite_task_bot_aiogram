from aiogram.types import Message

from loader import dp, _, bot
from services.user import get_all_user_id


@dp.message_handler(commands='users_count', is_admin=True)
async def users_count(message: Message, session):
    users = await get_all_user_id(session)

    count = len(users)

    active_count = 0
    for user in users:
        try:
            if await bot.send_chat_action(user, 'typing'):
                count += 1
        except Exception:
            pass

    await message.answer(_('Всего пользователей: {count}\n'
                           'Активных пользователей: {active_count}').format(count=count, active_count=active_count))

    await message.delete()

