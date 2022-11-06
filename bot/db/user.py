import datetime

from sqlalchemy import Column, VARCHAR, DATE, String

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(String, unique=True, nullable=False, primary_key=True)  # chat id + user id
    username = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DATE, default=datetime.date.today())
    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'
