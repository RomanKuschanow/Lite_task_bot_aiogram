from sqlalchemy import Column, Integer, BigInteger, DateTime, Boolean

from .base import db


class BannedUser(db):
    __tablename__ = 'banned_users'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)

    user_id = Column(BigInteger)

    ban_count = Column(Integer)

    banned_until = Column(DateTime)

    is_banned = Column(Boolean, default=False)
