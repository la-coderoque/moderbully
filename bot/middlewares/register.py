from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot import db
from bot.db import Chat, User


async def _group_register_check(event: Message, data: Dict[str, Any]):
    session_maker: sessionmaker = data['session_maker']
    chat = await db.get_chat(chat_id=event.chat.id,
                             session_maker=session_maker)
    user = await db.get_user(user_id=f'{event.chat.id}_{event.from_user.id}',
                             session_maker=session_maker)
    if not chat:
        await db.merge(Chat(chat_id=event.chat.id,
                            chatname=event.chat.username),
                       session_maker=session_maker)
    if not user:
        await db.merge(User(user_id=f'{event.chat.id}_{event.from_user.id}',
                            username=event.from_user.username,
                            can_send_voice_messages=True,
                            can_send_video_messages=True,
                            can_send_stickers=True),
                       session_maker=session_maker)


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
