from datetime import datetime
import re

from aiogram.types import Message

from services.user import get_referral, set_referral
from data.config import BOT_NAME
from loader import dp, _


@dp.message_handler(commands='referral')
async def get_referral_link(message: Message, session, user):
    referral_count = len(await get_referral(session, user.id))

    text = _("Вот твоя реферальная ссылка: {link}\n").format(link=f'http://t.me/{BOT_NAME}?start=referral_id_{user.id}')

    if referal_count < 10 and not user.is_vip and not user.is_admin:
        text += _("Пригласи 10 пользователей и получишь vip-статус.\n")
    else:
        text += _("У тебя уже есть vip-статус, но разработчики будут очень благодарны если ты продолжишь привлекать новых пользователей\n")

    text += _("Ты пригласил: {referral_count}").format(referral_count=referral_count)

    await message.answer(text)
    await message.delete()


@dp.message_handler(commands='start', text_startswith='/start referral_id')
async def use_referral_link(message: Message, user, session):
    args = message.get_args()
    id = int(re.search('referral_id_(\d+)', args)[1])

    if user.id != id and (datetime.now() - user.created_at).total_seconds() < 1:
        await set_referral(session, user.id, id)
        from bot.handlers.default.start import bot_start
        await bot_start(message)
    elif user.id == id:
        await message.answer(_("Ты не можешь использовать свою ссылку"))
        return
    elif (datetime.now() - user.created_at).total_seconds() > 1:
        await message.answer(_("Ты не можешь зарегистрироваться дважды"))
