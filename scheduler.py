from utils.misc.logging import logger
import time
from threading import Thread

import telebot

from data.config import BOT_TOKEN
from services.reminder import get_all_actual as get_all_actual_reminders, edit_repeating
from services.timer import get_all_actual as get_all_actual_timers, update_timer
from services.user import get_all_user_id

bot = telebot.TeleBot(BOT_TOKEN)


def reminders():
    while True:

        reminders_list = get_all_actual_reminders()

        if len(reminders_list) > 0:
            logger.info(reminders_list)

        for reminder in reminders_list:
            bot.send_message(reminder.user_id, reminder.text)

            edit_repeating(reminder.id, reminder.user_id, reminder.is_repeat)

        time.sleep(1)


def timers():
    while True:

        timers_list = get_all_actual_timers()

        if len(timers_list) > 0:
            logger.info(timers_list)

        for timer in timers_list:
            bot.send_message(timer.user_id, f"{timer.text}")

            update_timer(timer.user_id, timer.id, is_work=False)

        time.sleep(1)


def sender(text):
    users = list(get_all_user_id())

    i = int((len(users)) / 30) + 1

    while i > 0:

        for user in users[-30 * i:][:30] if i > 1 else users[:len(users) - int((len(users)) / 30)]:
            try:
                bot.send_message(user, text)
                logger.info(user)
            except:
                continue

        i -= 1

        time.sleep(1)


t_r = Thread(target=reminders)
t_t = Thread(target=timers)
