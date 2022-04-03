from aiogram.dispatcher.filters.builtin import Regexp
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.commands import set_user_commands
from bot.keyboards.default.menu import get_menu_keyboard_markup
from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _, i18n
from models import User
from services.user import edit_user_language


@dp.callback_query_handler(Regexp('^lang_(\w\w)$'))
async def change_language(callback_query: CallbackQuery, regexp: Regexp, session: AsyncSession, user: User):
    language = regexp.group(1)

    await edit_user_language(session, callback_query.from_user.id, language)
    i18n.set_user_locale(language)
    await set_user_commands(user.id, language)

    await callback_query.message.answer(_('Язык изменен\nНапиши /help чтобы узнать как я могу тебе помочь'),
                                        reply_markup=get_menu_keyboard_markup())
    await callback_query.message.delete()


@dp.message_handler(commands='lang')
async def bot_start(message: Message):
    text = _('Выберите свой язык')

    await message.answer(text, reply_markup=get_language_inline_markup())
