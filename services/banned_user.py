from sqlalchemy.ext.asyncio import AsyncSession

from models import BannedUser, User
from utils.misc import save_execute, save_commit


@save_execute
async def add_user_to_list(session: AsyncSession, user: User) -> BannedUser:
    user = BannedUser(user_id=user.id, ban_count=user.ban_count, banned_until=user.banned_until,
                      is_banned=user.is_banned)

    session.add(user)
    await save_commit(session)

    return user
