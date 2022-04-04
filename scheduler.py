import asyncio
from threading import Thread

import telebot

from data.config import BOT_TOKEN
from models.base import create_async_database
from services.reminder import get_all_actual, update_is_reminded
from services.user import get_all_user_id

bot = telebot.TeleBot(BOT_TOKEN)


async def reminders():
    session = await create_async_database()

    while True:
        for reminder in await get_all_actual(session):
            bot.send_message(reminder.user_id, reminder.text)
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
