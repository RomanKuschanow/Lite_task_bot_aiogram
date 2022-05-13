import json

from aiogram.types import User as tele_user
from pendulum import now

from data.config import ADMINS
from loader import bot, _
from models import User
from services.banned_user import add_user_to_list
from utils.misc.logging import logger


def create_user(user: tele_user) -> User:
    settings = {'kb_enabled': True, 'last_kb': 'main'}

    new_user = User.create(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name,
                           settings=json.dumps(settings))

    if user.id in ADMINS:
        new_user.is_admin = True
        new_user.save()

    logger.info(f'New user {new_user}')

    return new_user


def get_user(id: int) -> User:
    return User.get_or_none(User.id == id)


def set_referral(user_id, referal_id):
    query = User.update(referal_id=referal_id).where(User.id == user_id)
    query.execute()

    if len(get_referral(referal_id)) > 9:
        update_status(referal_id)


def get_referral(id: int) -> list[User]:
    return list(User.select(User).where(User.referal_id == id))


def get_user_language(id: int) -> str:
    return get_user(id).language


def get_all_users() -> list[User]:
    return list(User.select())


def get_all_user_id() -> list[int]:
    users = list(User.select(User.id))
    return [i.id for i in users]


def get_user_time_zone(id: int) -> str:
    return get_user(id).time_zone


def update_time_zone(id: int, time_zone: str):
    query = User.update(time_zone=time_zone).where(User.id == id)
    query.execute()


def update_status(id: int, is_vip: bool = True):
    query = User.update(is_vip=is_vip).where(User.id == id)
    query.execute()

    if is_vip:
        bot.send_message(id, _("Поздравляю! 🎉🎉🎉 Ты получил VIP-статус"))
    else:
        bot.send_message(id, _("У тебя забрали VIP-статус 😢"))


def update_is_admin(id: int, is_admin: bool = True):
    query = User.update(is_admin=is_admin).where(User.id == id)
    query.execute()

    if is_admin:
        bot.send_message(id, _("Поздравляю! 🎉🎉🎉 Теперь ты админ"))
    else:
        bot.send_message(id, _("Ты больше не админ 😢"))


def update_user(tele_user: tele_user) -> User:
    user = get_user(tele_user.id)
    user.first_name = tele_user.first_name
    user.last_name = tele_user.last_name
    user.username = tele_user.username

    if user.id in ADMINS:
        user.is_admin = True

    user.save()
    return user


def edit_user_language(id: int, language: str):
    query = User.update(language=language).where(User.id == id)
    query.execute()


def get_or_create_user(tele_user: tele_user) -> User:
    user = get_user(tele_user.id)

    if user:
        user = update_user(tele_user)

        return user

    return create_user(tele_user)


def ban_user(id: int) -> User:
    user = get_user(id)

    user.ban_count += 1
    user.banned_until = now().add(hours=(3 * user.ban_count))
    user.save()

    logger.info(f'User {id} banned')

    add_user_to_list(user)

    for admin in ADMINS:
        bot.send_message(admin, _('Пользователь {id} забанен').format(id=id))

    return user


def permanent_ban(id: int) -> User:
    user = get_user(id)

    user.is_banned = True
    user.save()

    logger.info(f'User {id} banned permanent')

    add_user_to_list(user)

    for admin in ADMINS:
        bot.send_message(admin, _('Пользователь {id} забанен навсегда').format(id=id))

    return user
