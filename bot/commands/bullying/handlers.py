from random import randrange
from datetime import timedelta

from aiogram.types import ChatMember, ChatPermissions, Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot import bot
from bot.db import User
from ..common import (apply_restriction, apply_restriction_to_sender,
                      change_reply_to_user_field, moderator_reply_to_condition)


async def cursed_command(message: Message, session_maker: sessionmaker) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await change_reply_to_user_field(message, attr='is_cursed', flag=True,
                                     session_maker=session_maker)
    await message.answer(f'User {message.reply_to_message.from_user.first_name} is cursed now')


async def uncursed_command(message: Message, session_maker: sessionmaker) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await change_reply_to_user_field(message, attr='is_cursed', flag=False,
                                     session_maker=session_maker)
    await message.answer(f'User {message.reply_to_message.from_user.first_name} is not cursed now')


async def despicable_command(message: Message, session_maker: sessionmaker) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await change_reply_to_user_field(message, attr='is_despicable', flag=True,
                                     session_maker=session_maker)
    await message.answer(f'User {message.reply_to_message.from_user.first_name} is despicable now')


async def undespicable_command(message: Message, session_maker: sessionmaker) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await change_reply_to_user_field(message, attr='is_despicable', flag=False,
                                     session_maker=session_maker)
    await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                         'is not despicable now')


async def shutup_command(message: Message, session_maker: sessionmaker) -> None:
    reply_to_user: ChatMember = await bot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
    ) if message.reply_to_message else None
    if not reply_to_user or reply_to_user.can_send_messages is False:
        return
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.reply_to_message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            despicable = getattr(user, 'is_despicable')
    if despicable:
        await apply_restriction(message=message,
                                permissions=ChatPermissions(can_send_messages=False),
                                duration=timedelta(seconds=600))


async def check_cursed(message: Message, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            cursed = getattr(user, 'is_cursed')
    part = randrange(2, 6)
    duration = randrange(3, 16) * 60
    if cursed and randrange(101) <= part:
        await apply_restriction_to_sender(message=message,
                                          permissions=ChatPermissions(can_send_messages=False),
                                          duration=timedelta(seconds=duration))
