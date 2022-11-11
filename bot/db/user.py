import datetime

from sqlalchemy import Boolean, Column, DATE, select, String, VARCHAR
from sqlalchemy.orm import sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(String, unique=True, nullable=False, primary_key=True)  # 'chatid_userid'
    username = Column(VARCHAR(32), unique=False, nullable=True)

    can_send_voice_messages = Column(Boolean, unique=False, nullable=False)
    can_send_video_messages = Column(Boolean, unique=False, nullable=False)
    can_send_stickers = Column(Boolean, unique=False, nullable=False)

    is_sheriff = Column(Boolean, unique=False, nullable=False)

    is_cursed = Column(Boolean, unique=False, nullable=False)
    is_despicable = Column(Boolean, unique=False, nullable=False)

    reg_date = Column(DATE, default=datetime.date.today())
    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'


async def get_user(user_id: str, session_maker: sessionmaker) -> User | None:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.user_id == user_id))
            return result.one_or_none()
