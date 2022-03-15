from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import ADMINS

from aiogram.types import User as tele_user

from models import User
from utils.misc.logging import logger
from bot.commands import set_default_commands


async def create_user(session: AsyncSession, user: tele_user) -> User:
    new_user = User(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)

    if str(user.id) in ADMINS:
        new_user.status = "admin"

    await set_default_commands()

    session.add(new_user)
    await session.commit()

    logger.info(f'New user {new_user}')

    return new_user


async def get_user(session: AsyncSession, id: int) -> User:
    sql = select(User).where(User.id == id)
    query = await session.execute(sql)

    user = query.scalar_one_or_none()

    return user


async def update_status(session: AsyncSession, id: int, status: str):
    sql = update(User).where(User.id == id).values(status=status)

    await session.execute(sql)

    try:
        await session.commit()
    except:
        await session.rollback()


async def update_user(session: AsyncSession, user: tele_user) -> User:
    updated_user = await get_user(session, user.id)

    updated_user.username = user.username
    updated_user.first_name = user.first_name
    updated_user.last_name = user.last_name

    await set_default_commands()

    try:
        await session.commit()
    except:
        await session.rollback()

    return updated_user


async def edit_user_language(session: AsyncSession, id: int, language: str):
    sql = update(User).where(User.id == id).values(language=language)

    await session.execute(sql)
    await session.commit()


async def get_or_create_user(session: AsyncSession, user: tele_user) -> User:
    new_or_get_user = await get_user(session, user.id)

    if new_or_get_user:
        new_or_get_user = await update_user(session, user)

        return new_or_get_user

    return await create_user(session, user)

