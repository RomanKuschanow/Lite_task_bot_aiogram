from datetime import datetime

import pytz
from pendulum import datetime as date_p, now

from models import Timer
from utils.misc.logging import logger


def create_timer(user, time: int, text: str = None) -> Timer:
    start_date = datetime.now()

    date = now().add(seconds=time + 1)
    end_date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

    new_timer = Timer.create(start_date=start_date, end_date=end_date, text=text, user=user)

    logger.info(f'New timer {new_timer}')

    return new_timer


def get_timer(id: int, user_id: int = None) -> Timer:
    if user_id is None:
        timer = Timer.get_or_none(Timer.id == id, Timer.is_work == True)
    else:
        timer = Timer.get_or_none(Timer.user_id == user_id, Timer.id == id, Timer.is_work == True)

    return timer


def get_all() -> list[Timer]:
    return list(Timer.select())


def get_all_actual() -> list[Timer]:
    return list(Timer.select().where(Timer.end_date < datetime.now(), Timer.is_paused == False,
                                     Timer.is_work == True))


def get_all_actual_by_user_id(user_id: int, *args) -> list[Timer]:
    return list(
        Timer.select().where(Timer.user_id == user_id, Timer.is_work == True).order_by(Timer.end_date))


def update_timer(user_id: int, id: int, **kwargs):
    query = Timer.update(kwargs).where(Timer.id == id, Timer.user_id == user_id)
    query.execute()


def pause(user_id: int, id: int) -> Timer:
    update_timer(user_id, id, is_paused=True, pause_date=datetime.now())
    return get_timer(id, user_id)


def play(user_id: int, id: int) -> Timer:
    timer = get_timer(id, user_id)

    s_date = now().subtract(seconds=(timer.pause_date - timer.start_date).total_seconds())
    e_date = now().add(seconds=(timer.end_date - timer.pause_date).total_seconds())

    end_date = datetime(e_date.year, e_date.month, e_date.day, e_date.hour, e_date.minute, e_date.second)
    start_date = datetime(s_date.year, s_date.month, s_date.day, s_date.hour, s_date.minute, s_date.second)

    update_timer(user_id, id, start_date=start_date, end_date=end_date, is_paused=False)

    return get_timer(id, user_id)
