from datetime import datetime

import pytz
from pendulum import datetime as date_p

from models import Reminder
from utils.misc.logging import logger
from .user import get_user_time_zone, get_user


def create_reminder(user_id: int, text: str, date: datetime, convert:bool = True) -> Reminder:
    if convert:
        localize_date = pytz.timezone(get_user_time_zone(user_id)).localize(date)

        d = localize_date.astimezone(pytz.UTC)

        server_date = datetime(d.year, d.month, d.day, d.hour, d.minute)
    else:
        server_date = date

    new_reminder = Reminder.create(text=text, date=server_date, next_date=server_date,
                                   is_reminded=server_date < datetime.now(), user=get_user(user_id))

    logger.info(f'New reminder {new_reminder}')

    return new_reminder


def get_reminder(id: int, user_id: int = None) -> Reminder:
    if user_id is None:
        reminder = Reminder.get_or_none(Reminder.id == id, Reminder.is_deleted == False)
    else:
        reminder = Reminder.get_or_none(Reminder.user_id == user_id, Reminder.id == id, Reminder.is_deleted == False)

    return reminder


def get_all() -> list[Reminder]:
    return list(Reminder.select())


def get_all_actual() -> list[Reminder]:
    return list(Reminder.select().where(Reminder.next_date < datetime.now(), Reminder.is_reminded == False,
                                Reminder.is_deleted == False))


def get_all_by_user_id(user_id: int, *args) -> list[Reminder]:
    return list(Reminder.select().where(Reminder.user_id == user_id, Reminder.is_deleted == False))


def get_all_old_by_user_id(user_id: int, *args) -> list[Reminder]:
    return list(Reminder.select().where(Reminder.user_id == user_id, Reminder.is_reminded == True, Reminder.is_deleted == False))


def get_all_actual_by_user_id(user_id: int, *args) -> list[Reminder]:
    return list(
        Reminder.select().where(Reminder.user_id == user_id, Reminder.is_reminded == False, Reminder.is_deleted == False))


def update_is_reminded(id: int, is_reminded: bool):
    query = Reminder.update(is_reminded=is_reminded).where(Reminder.id == id)
    query.execute()


def edit_text(id: int, text: str):
    query = Reminder.update(text=text).where(Reminder.id == id)
    query.execute()


def edit_date(id: int, user_id: int, date: datetime, use_tz: bool = True):
    if use_tz:
        localize_date = pytz.timezone(get_user_time_zone(user_id)).localize(date)

        d = localize_date.astimezone(pytz.UTC)

        server_date = datetime(d.year, d.month, d.day, d.hour, d.minute)
    else:
        server_date = date

    query = Reminder.update(date=server_date).where(Reminder.id == id)
    query.execute()

    reminder = get_reminder(id, user_id)
    edit_repeating(id, user_id, reminder.is_repeat)


def edit_repeating(id: int, user_id: int, is_repeat: bool = True):
    reminder = get_reminder(id, user_id)

    now_time = datetime.now()

    if is_repeat:
        date = date_p(reminder.date.year, reminder.date.month, reminder.date.day,
                      reminder.date.hour,
                      reminder.date.minute, tz=None)

        if reminder.repeat_count:
            if reminder.repeat_count == -1:
                while date < now_time:
                    date = get_date(reminder, date)
            else:
                i = 1
                while date < now_time and i < reminder.repeat_count:
                    date = get_date(reminder, date)
                    i += 1
                reminder.curr_repeat = i + int(i == reminder.repeat_count and date < now_time)
                reminder.save()
        if reminder.repeat_until:
            while date < now_time and date < reminder.repeat_until:
                date = get_date(reminder, date)
    else:
        date = reminder.date

    is_reminded = date < now_time

    reminder.is_repeat = is_repeat
    reminder.is_reminded = is_reminded
    reminder.next_date = datetime(date.year, date.month, date.day, date.hour, date.minute)
    reminder.save()


def edit_freely(id: int, user_id: int, edit_rep: bool = True, **kwargs) -> Reminder:
    if "repeat_until" in kwargs:
        if kwargs['repeat_until']:
            date = kwargs['repeat_until']
            naive = datetime(date.year, date.month, date.day, date.hour, date.minute)

            localize_date = pytz.timezone(get_user_time_zone(user_id)).localize(naive)

            d = localize_date.astimezone(pytz.UTC)

            kwargs['repeat_until'] = datetime(d.year, d.month, d.day, d.hour, d.minute)

    query = Reminder.update(kwargs).where(Reminder.id == id, Reminder.user_id == user_id)
    query.execute()

    if edit_rep:
        edit_repeating(id, user_id)

    return get_reminder(id, user_id)


def delete_reminder(user_id: int, id: int):
    query = Reminder.update(is_deleted=True).where(Reminder.user_id == user_id, Reminder.id == id)
    query.execute()


def true_delete_reminder(user_id: int, id: int):
    get_reminder(id, user_id).delete()


def get_date(reminder, start_date, step: int = 1) -> datetime:
    date = date_p(start_date.year, start_date.month, start_date.day,
                  start_date.hour,
                  start_date.minute, tz=None)

    if reminder.repeat_range == 'min':
        date = date.add(minutes=step)

    if reminder.repeat_range == 'day':
        date = date.add(days=step)

    if reminder.repeat_range == 'week':
        date = date.add(weeks=step)

    if reminder.repeat_range == 'month':
        date = date.add(months=step)

    if reminder.repeat_range == 'year':
        date = date.add(years=step)

    return date
