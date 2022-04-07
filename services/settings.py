from aiogram.types import User as tele_user
from pendulum import now
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import ADMINS
from loader import bot, _
from models import User, Settings
from utils.misc import save_execute, save_commit
from services.banned_user import add_user_to_list
from utils.misc.logging import logger


@save_execute
async def create_user_settings(session: AsyncSession, user_id: int) -> Settings:
    settings = Settings(user_id=user_id)

    session.add(settings)
    await save_commit(session)

    return settings


@save_execute
async def get_settings(session: AsyncSession, user_id: int) -> Settings:
    sql = select(Settings).where(user_id == user_id)
    query = await session.execute(sql)
    
    settings = query.scalar_one_or_none()
    
    return settings


@save_execute
async def update_settings(session: AsyncSession, settings: Settings):
    updated_settings = await get_settings(session, settings.user_id)

    updated_settings.kb_enabled = settings.kb_enabled
    updated_settings.last_kb = settings.last_kb

    await save_commit(session)


@save_execute
async def get_or_crate_settings(session: AsyncSession, user_id: int) -> Settings:
    settings = await get_settings(session, user_id)

    if settings:
        return settings
    else:
        return await create_user_settings(session, user_id)



