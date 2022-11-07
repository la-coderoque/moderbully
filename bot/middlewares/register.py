from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.db import User, Chat


async def _group_register_check(event: Message, data: Dict[str, Any]):
    session_maker: sessionmaker = data['session_maker']
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Chat).where(Chat.chat_id == event.chat.id)
            )
            chat = result.one_or_none()
            if chat is not None:
                pass
            else:
                chat = Chat(
                    chat_id=event.chat.id,
                    chatname=event.chat.username,
                )
                await session.merge(chat)

            result = await session.execute(
                select(User).where(User.user_id == f'{event.chat.id}_{event.from_user.id}')
            )
            user = result.one_or_none()

            if user is not None:
                pass
            else:
                user = User(
                    user_id=f'{event.chat.id}_{event.from_user.id}',
                    username=event.from_user.username,
                )
                await session.merge(user)


class GroupRegisterCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.chat.type not in ('private', 'channel'):
            await _group_register_check(event, data)
        return await handler(event, data)
