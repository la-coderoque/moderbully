from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import ChatMember, Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.db import User
from bot.utils.time import parse_timedelta, TimedeltaParseError

DEFAULT_TD = 15  # minutes


class BaseAction(ABC):
    _moderator_statuses = ('creator', 'administrator')

    def __init__(self, bot: Bot, message: Message,
                 session_maker: sessionmaker,
                 command: Optional[CommandObject] = None) -> None:
        self.bot = bot
        self.message = message
        self.session_maker = session_maker
        self.command = command

    @property
    def sender_tg_id(self) -> int:
        return self.message.from_user.id

    @property
    def reply_to_user_tg_id(self) -> int | None:
        if not self.message.reply_to_message:
            return
        return self.message.reply_to_message.from_user.id

    async def parse_timedelta_from_message(self) -> timedelta | None:
        if args := getattr(self.command, 'args'):
            try:
                duration = parse_timedelta(args.split()[0])
            except TimedeltaParseError:
                await self.message.reply('Failed to parse duration')
                return
            if duration <= timedelta(seconds=30):
                return timedelta(seconds=30)
            return duration
        return timedelta(minutes=DEFAULT_TD)

    async def is_user_moderator(self, user_tg_id: int) -> bool:
        user: ChatMember = await self.bot.get_chat_member(chat_id=self.message.chat.id,
                                                          user_id=user_tg_id)
        return user.status in self._moderator_statuses

    async def is_user_sheriff(self, user_tg_id: int) -> bool:
        async with self.session_maker() as session:
            async with session.begin():
                user_bot_id = f'{self.message.chat.id}_{user_tg_id}'
                result = await session.execute(select(User).where(User.user_id == user_bot_id))
                user: User = result.scalars().unique().one_or_none()
                return bool(user.is_sheriff)

    async def moderator_reply_condition(self) -> bool:
        if not self.reply_to_user_tg_id:
            return False
        sender_is_moderator = await self.is_user_moderator(self.sender_tg_id)
        reply_to_user_is_moderator = await self.is_user_moderator(self.reply_to_user_tg_id)
        return sender_is_moderator and not reply_to_user_is_moderator

    async def sheriff_reply_condition(self) -> bool:
        if not self.reply_to_user_tg_id or await self.is_user_moderator(self.reply_to_user_tg_id):
            return False
        sender_is_sheriff = await self.is_user_sheriff(self.sender_tg_id)
        reply_to_user_is_sheriff = await self.is_user_sheriff(self.reply_to_user_tg_id)
        return sender_is_sheriff and not reply_to_user_is_sheriff

    @abstractmethod
    def make(self):
        pass
