from aiogram.dispatcher.filters.builtin import Regexp
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.commands import set_user_commands, set_admin_commands
from bot.keyboards.default.set_menu import set_menu
from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _, i18n
from models import User
from services.user import edit_user_language


@dp.callback_query_handler(Regexp('^lang_(\w\w)$'), state='*')
async def change_language(callback_query: CallbackQuery, regexp: Regexp, session: AsyncSession, user: User, state):
    language = regexp.group(1)

    await edit_user_language(session, callback_query.from_user.id, language)
    i18n.set_user_locale(language)

    if user.is_admin:
        await set_admin_commands(user.id, language)
    else:
        await set_user_commands(user.id, language)

    async with state.proxy() as data:
        if data.state == 'Start:lang':
            text = _(
                'Привет, я Task Bot. Ты можешь составить список задач, а я в назначенное время напомню тебе о них.\n'
                'Пока что функционал у меня ограничен простыми напоминаниями, '
                'но в грядущих обновлениях мои возможности сильно возрастут.\n'
                'Теперь ты можешь написать /help, чтобы узнать чем я могу тебе помочь.\n'
                'Так же рекомендую выбрать часовой пояс, если он не соответствует киевскому: /tz')
        else:
            text = _('Язык изменен\nНапиши /help чтобы узнать как я могу тебе помочь')

    await state.finish()

    await callback_query.message.answer(text, reply_markup=set_menu(user))
    await callback_query.message.delete()


@dp.message_handler(commands='lang')
async def lang(message: Message):
    text = _('Выберите свой язык')

    await message.answer(text, reply_markup=get_language_inline_markup())
    await message.delete()
