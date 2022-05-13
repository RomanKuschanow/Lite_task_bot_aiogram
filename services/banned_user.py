from models import BannedUser, User


def add_user_to_list(user: User) -> BannedUser:
    user = BannedUser.create(user_id=user.id, ban_count=user.ban_count, banned_until=user.banned_until,
                             is_banned=user.is_banned)
    return user
