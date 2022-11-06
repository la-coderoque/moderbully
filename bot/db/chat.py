import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE

from .base import BaseModel


class Chat(BaseModel):
    __tablename__ = 'chats'

    chat_id = Column(Integer, unique=True, nullable=False, primary_key=True)  # tg chat id
    chatname = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DATE, default=datetime.date.today())
    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f'<Chat:{self.user_id}>'
