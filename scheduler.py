from threading import Thread
from time import sleep
from services.reminder import get_all_actual, update_is_reminded
from datetime import datetime
from models.base import create_async_database
import asyncio
import telebot
from data.config import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)

async def scheduler():
    session = await create_async_database()

    while True:
        for reminder in await get_all_actual(session):
                bot.send_message(reminder.user_id, reminder.text)
                await update_is_reminded(session, reminder.id, True)

        await asyncio.sleep(1)


def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(scheduler())
    loop.close()


t = Thread(target=between_callback)
