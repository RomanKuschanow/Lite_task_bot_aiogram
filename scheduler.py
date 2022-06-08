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
            try:
                bot.send_message(reminder.user_id, reminder.text)

                logger.info("maybe, bot was blocked by the user")
            except:

            edit_repeating(reminder.id, reminder.user_id, reminder.is_repeat)

        time.sleep(1)


def timers():
    while True:

        timers_list = get_all_actual_timers()

        if len(timers_list) > 0:
            logger.info(timers_list)

        for timer in timers_list:
            try:
                bot.send_message(timer.user_id, f"{timer.text}")
            except:
                logger.info("maybe, bot was blocked by the user")

            update_timer(timer.user_id, timer.id, is_work=False)
        time.sleep(1)


def sender(text):
    user_ids = list(get_all_user_id())

    for user_id in user_ids:
        try:
            bot.send_message(user_id, text)
            logger.info(user_id)
        except:
            pass


t_r = Thread(target=reminders)
t_t = Thread(target=timers)
