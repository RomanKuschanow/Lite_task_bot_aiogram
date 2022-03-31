from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from models.tasks import Task
from utils.misc.logging import logger


def create_task(session: AsyncSession, user_id: int, text: str, end_date: datetime = None, priority: int = 0) -> Task:
    new_task = Task(user_id=user_id, text=text, end_date=end_date, priority=priority)

    session.add(new_task)
    await save_commit(session)

    logger.info(f'New task {new_task}')

    return new_task


def get_task(session: AsyncSession, id: int, user_id: int = None) -> Task:
    if user_id is None:
        sql = select(Task).where(Task.id == id)
    else:
        sql = select(Task).where(Task.user_id == user_id, Task.id == id)

    query = await session.execute(sql)

    task = query.scalar_one_or_none()

    return task


def get_all_sorted_by(session: AsyncSession, user_id: int, sort, order=Task.end_date.asc) -> list[Task]:
    sql = select(Task).where(sort()).order_by(order())
    query = await session.execute(sql)

    return [t for t, in query]


def get_all_by_user_id(session: AsyncSession, user_id: int) -> list[Task]:
    sql = select(Task).where(Task.user_id == user_id)
    query = await session.execute(sql)

    return [t for t, in query]


def delete_task(session: AsyncSession, user_id: int, id: int):
    sql = update(Task).where(Task.user_id == user_id, Task.id == id).values(is_deleted=True)
    query = await session.execute(sql)

    await save_commit(session)


@save_execute
async def true_delete_reminder(session: AsyncSession, user_id: int, id: int):
    sql = delete(Task).where(Task.user_id == user_id, Task.id == id)
    query = await session.execute(sql)

    await save_commit(session)


def delete_all_by_user_id(session: AsyncSession, user_id: int):
    sql = delete(Task).where(Task.user_id == user_id)
    query = await session.execute(sql)

    await save_commit(session)
