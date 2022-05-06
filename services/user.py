from aiogram.types import User as tele_user
from pendulum import now
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import ADMINS
from loader import bot, _
from models import User
from utils.misc import save_execute, save_commit
from services.banned_user import add_user_to_list
from utils.misc.logging import logger


@save_execute
async def create_user(session: AsyncSession, user: tele_user) -> User:
    new_user = User(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)

    if user.id in ADMINS:
        new_user.is_admin = True

    session.add(new_user)
    await save_commit(session)

    from .settings import create_user_settings

    await create_user_settings(session, new_user.id)

    logger.info(f'New user {new_user}')

    return new_user


@save_execute
async def get_user(session: AsyncSession, id: int) -> User:
    sql = select(User).where(User.id == id)
    query = await session.execute(sql)

    user = query.scalar_one_or_none()

    return user


@save_execute
async def set_referral(session: AsyncSession, user_id, referal_id):
    sql = update(User).where(User.id == user_id).values(referal_id=referal_id)

    await session.execute(sql)

    await save_commit(session)

    if len(await get_referral(session, referal_id)) > 9:
        await update_status(session, referal_id)


@save_execute
async def get_referral(session: AsyncSession, id: int) -> list[User]:
    sql = select(User).where(User.referal_id == id)
    query = await session.execute(sql)

    return [u for u, in query]


@save_execute
async def get_user_language(session: AsyncSession, id: int) -> str:
    sql = select(User).where(User.id == id)
    query = await session.execute(sql)

    user = query.scalar_one_or_none()

    return user.language


@save_execute
async def get_all_users(session: AsyncSession) -> list[User]:
    sql = select(User)
    query = await session.execute(sql)

    return [u for u, in query]


@save_execute
async def get_all_user_id(session: AsyncSession) -> list[User]:
    sql = select(User.id)
    query = await session.execute(sql)

    return [u for u, in query]


@save_execute
async def get_user_time_zone(session: AsyncSession, id: int) -> str:
    user = await get_user(session, id)

    return user.time_zone


@save_execute
async def update_time_zone(session: AsyncSession, id: int, time_zone: str):
    sql = update(User).where(User.id == id).values(time_zone=time_zone)

    await session.execute(sql)

    await save_commit(session)


@save_execute
async def update_status(session: AsyncSession, id: int, is_vip: bool = True):
    sql = update(User).where(User.id == id).values(is_vip=is_vip)

    await session.execute(sql)

    if is_vip:
        await bot.send_message(id, _("Поздравляю! 🎉🎉🎉 Ты получил VIP-статус"))
    else:
        await bot.send_message(id, _("У тебя забрали VIP-статус 😢"))

    await save_commit(session)


@save_execute
async def update_is_admin(session: AsyncSession, id: int, is_admin: bool = True):
    sql = update(User).where(User.id == id).values(is_admin=is_admin)

    await session.execute(sql)

    if is_admin:
        await bot.send_message(id, _("Поздравляю! 🎉🎉🎉 Теперь ты админ"))
    else:
        await bot.send_message(id, _("Ты больше не админ 😢"))

    await save_commit(session)


@save_execute
async def update_user(session: AsyncSession, user: tele_user) -> User:
    updated_user = await get_user(session, user.id)

    updated_user.username = user.username
    updated_user.first_name = user.first_name
    updated_user.last_name = user.last_name

    if user.id in ADMINS:
        updated_user.is_admin = True

    await save_commit(session)

    return updated_user


@save_execute
async def edit_user_language(session: AsyncSession, id: int, language: str):
    sql = update(User).where(User.id == id).values(language=language)

    await session.execute(sql)
    await save_commit(session)


@save_execute
async def get_or_create_user(session: AsyncSession, tele_user: tele_user) -> User:
    user = await get_user(session, tele_user.id)

    if user:
        user = await update_user(session, tele_user)

        return user

    return await create_user(session, tele_user)


@save_execute
async def ban_user(session: AsyncSession, id: int) -> User:
    user = await get_user(session, id)

    user.ban_count += 1
    user.banned_until = now().add(hours=(3 * user.ban_count))

    await save_commit(session)

    logger.info(f'User {id} banned')

    await add_user_to_list(session, user)

    for admin in ADMINS:
        await bot.send_message(admin, _('Пользователь {id} забанен').format(id=id))

    return user


@save_execute
async def permanent_ban(session: AsyncSession, id: int) -> User:
    user = await get_user(session, id)

    user.is_banned = True

    await save_commit(session)

    logger.info(f'User {id} banned permanent')

    await add_user_to_list(session, user)

    for admin in ADMINS:
        await bot.send_message(admin, _('Пользователь {id} забанен навсегда').format(id=id))

    return user
