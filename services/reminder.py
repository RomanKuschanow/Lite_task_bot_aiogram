from datetime import datetime

import pytz
from pendulum import datetime as date_p
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Reminder
from utils.misc import save_execute, save_commit
from utils.misc.logging import logger
from .user import get_user_time_zone


@save_execute
async def create_reminder(session: AsyncSession, user_id: int, text: str, date: datetime) -> Reminder:
    localize_date = pytz.timezone(await get_user_time_zone(session, user_id)).localize(date)

    d = localize_date.astimezone(pytz.UTC)

    server_date = datetime(d.year, d.month, d.day, d.hour, d.minute)

    new_reminder = Reminder(user_id=user_id, text=text, date=server_date, next_date=server_date,
                            is_reminded=server_date < datetime.now())

    session.add(new_reminder)
    await save_commit(session)

    logger.info(f'New reminder {new_reminder}')

    return new_reminder


@save_execute
async def get_reminder(session: AsyncSession, id: int, user_id: int = None) -> Reminder:
    if user_id is None:
        sql = select(Reminder).where(Reminder.id == id, Reminder.is_deleted == False)
    else:
        sql = select(Reminder).where(Reminder.user_id == user_id, Reminder.id == id, Reminder.is_deleted == False)

    query = await session.execute(sql)

    reminder = query.scalar_one_or_none()

    return reminder


@save_execute
async def get_all(session: AsyncSession) -> list[Reminder]:
    sql = select(Reminder)
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_actual(session: AsyncSession) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.next_date < datetime.now(), Reminder.is_reminded == False,
                                 Reminder.is_deleted == False)
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_by_user_id(session: AsyncSession, user_id: int, *args) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.user_id == user_id, Reminder.is_deleted == False).order_by(
        Reminder.next_date.asc())
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_old_by_user_id(session: AsyncSession, user_id: int, *args) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.is_reminded == True, Reminder.user_id == user_id,
                                 Reminder.is_deleted == False).order_by(Reminder.next_date.asc())
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_actual_by_user_id(session: AsyncSession, user_id: int, *args) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.is_reminded == False, Reminder.user_id == user_id,
                                 Reminder.is_deleted == False).order_by(Reminder.next_date.asc())
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def update_is_reminded(session: AsyncSession, id: int, is_reminded: bool):
    sql = update(Reminder).where(Reminder.id == id).values(is_reminded=is_reminded)

    await session.execute(sql)

    await save_commit(session)


@save_execute
async def edit_text(session: AsyncSession, id: int, text: str):
    sql = update(Reminder).where(Reminder.id == id).values(text=text)

    await session.execute(sql)

    await save_commit(session)


@save_execute
async def edit_date(session: AsyncSession, id: int, user_id: int, date: datetime, use_tz: bool = True):
    if use_tz:
        localize_date = pytz.timezone(await get_user_time_zone(session, user_id)).localize(date)

        d = localize_date.astimezone(pytz.UTC)

        server_date = datetime(d.year, d.month, d.day, d.hour, d.minute)
    else:
        server_date = date

    sql = update(Reminder).where(Reminder.id == id).values(date=server_date)

    await session.execute(sql)

    await save_commit(session)

    reminder = await get_reminder(session, id, user_id)
    await edit_repeating(session, id, user_id, reminder.is_repeat)


@save_execute
async def edit_repeating(session: AsyncSession, id: int, user_id: int, is_repeat: bool = True):
    reminder = await get_reminder(session, id, user_id)

    now_time = datetime.now()

    if is_repeat:
        date = date_p(reminder.date.year, reminder.date.month, reminder.date.day,
                      reminder.date.hour,
                      reminder.date.minute, tz=None)


        if reminder.repeat_count:
            if reminder.repeat_count == -1:
                while date < now_time:
                    date = await get_date(reminder, date)
            else:
                i = 1
                while date < now_time and i < reminder.repeat_count:
                    date = await get_date(reminder, date)
                    i += 1
                reminder.curr_repeat = i + int(i == reminder.repeat_count and date < now_time)
                await save_commit(session)
        if reminder.repeat_until:
            while date < now_time and date < reminder.repeat_until:
                date = await get_date(reminder, date)
    else:
        date = reminder.date

    is_reminded = date < now_time

    sql = update(Reminder).where(Reminder.id == id, Reminder.user_id == user_id).values(is_repeat=is_repeat,
                                                                                        is_reminded=is_reminded,
                                                                                        next_date=datetime(date.year,
                                                                                                           date.month,
                                                                                                           date.day,
                                                                                                           date.hour,
                                                                                                           date.minute))

    await session.execute(sql)

    await save_commit(session)


@save_execute
async def edit_freely(session: AsyncSession, id: int, user_id: int, edit_rep: bool = True, **kwargs) -> Reminder:
    if "repeat_until" in kwargs:
        if kwargs['repeat_until']:
            date = kwargs['repeat_until']
            naive = datetime(date.year, date.month, date.day, date.hour, date.minute)

            localize_date = pytz.timezone(await get_user_time_zone(session, user_id)).localize(naive)

            d = localize_date.astimezone(pytz.UTC)

            kwargs['repeat_until'] = datetime(d.year, d.month, d.day, d.hour, d.minute)

    sql = update(Reminder).where(Reminder.id == id, Reminder.user_id == user_id).values(kwargs)

    await session.execute(sql)

    await save_commit(session)

    if edit_rep:
        await edit_repeating(session, id, user_id)

    return await get_reminder(session, id, user_id)


@save_execute
async def delete_reminder(session: AsyncSession, user_id: int, id: int):
    sql = update(Reminder).where(Reminder.user_id == user_id, Reminder.id == id).values(is_deleted=True)
    query = await session.execute(sql)

    await save_commit(session)


@save_execute
async def true_delete_reminder(session: AsyncSession, user_id: int, id: int):
    sql = delete(Reminder).where(Reminder.user_id == user_id, Reminder.id == id)
    query = await session.execute(sql)

    await save_commit(session)


@save_execute
async def delete_all_by_user_id(session: AsyncSession, user_id: int):
    sql = delete(Reminder).where(Reminder.user_id == user_id)
    query = await session.execute(sql)

    await save_commit(session)


async def get_date(reminder, start_date, step: int = 1) -> datetime:
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
