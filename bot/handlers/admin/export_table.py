import csv

from aiogram.types import Message, InputFile

from loader import dp, _, config

from bot.keyboards.inline import get_export_inline_markup
from services.user import get_all_users


@dp.message_handler(commands='export_table', is_admin=True)
async def export_table(message: Message):
    await message.answer(_("Выбери таблицу для экспорта"), reply_markup=get_export_inline_markup())
    await message.delete()


@dp.callback_query_handler(text_startswith="export:users")
async def select_table(callback_query, session):
    await callback_query.answer()

    users = await get_all_users(session)

    count = len(users)

    file_path = config.DIR / 'users.csv'
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['id', 'first_name', 'last_name', 'username', 'is_vip', 'language', 'created_at'])

        for user in users:
            writer.writerow([user.id, user.first_name, user.last_name, user.username, user.is_vip, user.language, user.created_at])

    text_file = InputFile(file_path, filename='users.csv')
    await callback_query.message.answer_document(text_file, caption=_('Всего пользователей: {count}').format(count=count))

