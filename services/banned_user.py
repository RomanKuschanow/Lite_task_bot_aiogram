from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import BannedUser, User
from utils.misc.logging import logger


async def add_user_to_list(session: AsyncSession, user: User) -> BannedUser:
    user = BannedUser(user_id=user.id, ban_count=user.ban_count, banned_until=user.banned_until)

    session.add(user)
    await session.commit()

    return user

