import datetime

from sqlalchemy import BigInteger, Column, DATE, select, VARCHAR
from sqlalchemy.orm import sessionmaker

from .base import BaseModel


class Chat(BaseModel):
    __tablename__ = 'chats'

    chat_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)  # tg chat id
    chatname = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DATE, default=datetime.date.today())
    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f'<Chat:{self.user_id}>'


async def get_chat(chat_id: int, session_maker: sessionmaker) -> Chat | None:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Chat).where(Chat.chat_id == chat_id))
            return result.one_or_none()
