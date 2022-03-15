from sqlalchemy import Column, Integer, BigInteger, String

from base import db


class Timetable(db):
    __tablename__ = 'timetable'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(BigInteger)

    day = Column(String)
    task = Column(String)

    def __repr__(self) -> str:
        return f'[{get_user(self.user_id)}] {self.week}'
