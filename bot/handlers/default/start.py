from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from bot.keyboards.default import set_default_markup
from utils.misc import rate_limit

from loader import dp, _


@dp.message_handler(CommandStart())
@rate_limit(5, 'bot_start')
async def bot_start(message: Message, user):
    args = message.get_args()

    if not args:
        text = _("Привет, я Task Bot. Я помогу тебе с планами на день, неделю, месяц.... жизнь 😉\n" \
            "Если хочешь пройти небольшой экскурс по основным функциям, напиши /help, а для инфорамции о всех командах напиши /commands_list")

        await message.answer(text)

