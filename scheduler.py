import asyncio
from datetime import datetime
from threading import Thread

import telebot
from pendulum import datetime as date_p

from data.config import BOT_TOKEN
from models.base import create_async_database
from services.reminder import get_all_actual, update_is_reminded, edit_date, edit_freely
from services.user import get_all_user_id

bot = telebot.TeleBot(BOT_TOKEN)


async def reminders():
    session = await create_async_database()

    while True:
        for reminder in await get_all_actual(session):
            bot.send_message(reminder.user_id, reminder.text)

            if reminder.is_repeat:
                if (reminder.repeat_count and reminder.repeat_count == reminder.curr_repeat):
                    await update_is_reminded(session, reminder.id, True)
                else:
                    date = date_p(reminder.next_date.year, reminder.next_date.month, reminder.next_date.day,
                                  reminder.next_date.hour,
                                  reminder.next_date.minute, tz=None)

                    if reminder.repeat_range == 'min':
                        date = date.add(minutes=1)

                    if reminder.repeat_range == 'day':
                        date = date.add(days=1)

                    if reminder.repeat_range == 'week':
                        date = date.add(weeks=1)

                    if reminder.repeat_range == 'month':
                        date = date.add(months=1)

                    if reminder.repeat_range == 'year':
                        date = date.add(years=1)

                    if reminder.repeat_until and date > reminder.repeat_until:
                        await update_is_reminded(session, reminder.id, True)
                        continue
                    else:
                        await edit_date(session, reminder.id, reminder.user_id,
                                        datetime(date.year, date.month, date.day, date.hour, date.minute), False)
                        await edit_freely(session, reminder.id, reminder.user_id,
                                                   curr_repeat=reminder.curr_repeat + 1)
            else:
                await update_is_reminded(session, reminder.id, True)

        await asyncio.sleep(1)


async def sender(text):
    session = await create_async_database()

    users = list(await get_all_user_id(session))

    i = int((len(users)) / 30) + 1

    while i > 0:

        for user in users[-30 * i:][-30:]:
            bot.send_message(user, text)

        i -= 1

        await asyncio.sleep(1)


def between_callback(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if len(args) == 0:
        loop.run_until_complete(func())
    else:
        loop.run_until_complete(func(args))
    loop.close()


t = Thread(target=between_callback, args=(reminders,))
