import csv

from aiogram.types import Message, InputFile

from loader import dp, _, config

from bot.keyboards.inline import get_export_inline_markup
from services.reminder import get_all
from services.user import get_all_users


@dp.message_handler(commands='export_table', is_admin=True)
async def export_table(message: Message):
    await message.answer(_("Выбери таблицу для экспорта"), reply_markup=get_export_inline_markup())
    await message.delete()


@dp.callback_query_handler(text_startswith="export:users")
async def select_table_users(callback_query):
    await callback_query.answer()

    users = get_all_users()

    count = len(users)

    file_path = config.DIR / 'users.csv'
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['id', 'first_name', 'last_name', 'username', 'is_vip', 'referral_id', 'language', 'created_at'])

        for user in users:
            writer.writerow([user.id, user.first_name, user.last_name, user.username, user.is_vip, user.referal_id, user.language,
                             user.created_at])

    text_file = InputFile(file_path, filename='users.csv')
    await callback_query.message.answer_document(text_file, caption=_('Всего пользователей: {count}').format(count=count))


@dp.callback_query_handler(text_startswith="export:reminders")
async def select_table_reminders(callback_query):
    await callback_query.answer()

    reminders = get_all()

    count = len(reminders)

    file_path = config.DIR / 'reminders.csv'
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['id', 'user', 'text', 'date', 'is_reminded', 'is_repeat', 'is_deleted', 'repeat_until', 'repeat_range',
                         'repeat_count'])

        for reminder in reminders:
            writer.writerow([reminder.id, reminder.user, reminder.text, reminder.date, reminder.is_reminded, reminder.is_repeat,
                             reminder.is_deleted, reminder.repeat_until, reminder.repeat_range, reminder.repeat_count])

    text_file = InputFile(file_path, filename='reminders.csv')
    await callback_query.message.answer_document(text_file, caption=_('Всего напоминаний: {count}').format(count=count))
