from datetime import datetime

import pytz
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

    new_reminder = Reminder(user_id=user_id, text=text, date=server_date)

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

    return


@save_execute
async def get_all_actual(session: AsyncSession) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.date < datetime.now(), Reminder.is_reminded == False,
                                 Reminder.is_deleted == False)
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_by_user_id(session: AsyncSession, user_id: int, *args) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.user_id == user_id, Reminder.is_deleted == False).order_by(
        Reminder.date.asc())
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_old_by_user_id(session: AsyncSession, user_id: int, *args) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.is_reminded == True, Reminder.user_id == user_id,
                                 Reminder.is_deleted == False).order_by(Reminder.date.asc())
    query = await session.execute(sql)

    return [r for r, in query]


@save_execute
async def get_all_actual_by_user_id(session: AsyncSession, user_id: int, *args) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.is_reminded == False, Reminder.user_id == user_id,
                                 Reminder.is_deleted == False).order_by(Reminder.date.asc())
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
async def edit_date(session: AsyncSession, id: int, user_id, date: datetime):
    localize_date = pytz.timezone(await get_user_time_zone(session, user_id)).localize(date)

    d = localize_date.astimezone(pytz.UTC)

    server_date = datetime(d.year, d.month, d.day, d.hour, d.minute)

    sql = update(Reminder).where(Reminder.id == id).values(date=server_date)

    await session.execute(sql)

    await save_commit(session)


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
