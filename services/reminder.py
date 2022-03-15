from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Reminder

from datetime import datetime

from utils.misc.logging import logger


async def create_reminder(session: AsyncSession, user_id: int, text: str, date: datetime) -> Reminder:
    new_reminder = Reminder(user_id=user_id, text=text, date=date)

    session.add(new_reminder)
    await session.commit()

    logger.info(f'New reminder {new_reminder}')

    return new_reminder


async def get_reminder(session: AsyncSession, id: int, user_id: int = None) -> Reminder:
    if user_id is None:
        sql = select(Reminder).where(Reminder.id == id)
    else:
        sql = select(Reminder).where(Reminder.user_id == user_id, Reminder.id == id)

    query = await session.execute(sql)

    reminder = query.scalar_one_or_none()

    return reminder


async def get_all_by_user_id(session: AsyncSession, user_id: int) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.user_id == user_id)
    query = await session.execute(sql)

    return [r for r, in query]


async def get_all() -> list[Reminder]:
    sql = select(Reminder)
    query = await session.execute(sql)

    return [r for r, in query]


async def get_all_actual(session: AsyncSession, ) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.is_reminded == False)
    query = await session.execute(sql)

    return [r for r, in query]


async def get_all_actual_by_user_id(session: AsyncSession, user_id: int) -> list[Reminder]:
    sql = select(Reminder).where(Reminder.is_reminded == False, Reminder.user_id == user_id)
    query = await session.execute(sql)

    return [r for r, in query]


async def update_is_reminded(session: AsyncSession, id: int, is_reminded: bool):
    sql = update(Reminder).where(Reminder.id == id).values(is_reminded=is_reminded)

    await session.execute(sql)

    try:
        await session.commit()
    except:
        await session.rollback()


async def edit(session: AsyncSession, id: int, text: str, date: datetime):
    reminder = get_reminder_by_id(session, sid)

    reminder.text = text
    reminder.date = date

    try:
        await session.commit()
    except:
        await session.rollback()


async def delete_reminder(session: AsyncSession, user_id: int, id: int):
    sql = delete(Reminder).where(Reminder.user_id == user_id, Reminder.id == id)
    query = await session.execute(sql)

    await session.commit()


async def delete_all_by_user_id(session: AsyncSession, user_id: int):
    sql = delete(Reminder).where(Reminder.user_id == user_id)
    query = await session.execute(sql)

    await session.commit()

