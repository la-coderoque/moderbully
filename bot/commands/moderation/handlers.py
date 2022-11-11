from aiogram.types import (ChatPermissions, Message)
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot import bot
from bot.utils.time import (parse_timedelta_from_message, random_time_in_range,
                            td_format, DEFAULT_TD)
from ..common import apply_restriction, moderator_reply_to_condition
from bot.db import User


# check permissions
async def check_user_permissions(message: Message, session_maker: sessionmaker):
    pass


# read only
async def read_only_command(message: Message) -> None:
    if not await moderator_reply_to_condition(message):
        return
    duration = await parse_timedelta_from_message(message)
    if not duration:
        return
    await apply_restriction(message=message,
                            permissions=ChatPermissions(can_send_messages=False),
                            duration=duration)


async def random_read_only_command(message: Message) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await apply_restriction(message=message,
                            permissions=ChatPermissions(can_send_messages=False),
                            duration=timedelta(seconds=random_time_in_range(0, 24)))


# ban
async def ban_command(message: Message) -> None:
    if not await moderator_reply_to_condition(message):
        return
    duration = await parse_timedelta_from_message(message)
    if not duration:
        return
    elif duration.seconds == DEFAULT_TD * 60:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
        )
        await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                             '<b>banned</b> forever')
    else:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            until_date=duration,
        )
        await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                             f'<b>banned</b> for {td_format(duration) or " "}')


async def ban_sender_chat_command(message: Message) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await bot.ban_chat_sender_chat(chat_id=message.chat.id,
                                   sender_chat_id=message.reply_to_message.sender_chat.id)
    await message.answer(f'Channel {message.reply_to_message.sender_chat.title} '
                         '<b>banned</b> forever')


# unmute|unban
async def unmute_command(message: Message) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        only_if_banned=True,
    )
    await apply_restriction(message=message,
                            permissions=ChatPermissions(can_send_messages=True))
    await message.answer(f'User {message.reply_to_message.from_user.first_name} unrestricted')


async def unban_sender_chat_command(message: Message) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await bot.unban_chat_sender_chat(chat_id=message.chat.id,
                                     sender_chat_id=message.reply_to_message.sender_chat.id)
    await message.answer(f'Channel {message.reply_to_message.sender_chat.title} <b>unbanned</b>')


# media
async def _restrict_media(message: Message, attr: str, flag: bool,
                          session_maker: sessionmaker,
                          answer_substring: str = '') -> None:
    if not await moderator_reply_to_condition(message):
        return
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.reply_to_message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            setattr(user, attr, flag)
            await session.merge(user)
    if answer_substring:
        await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                             f"can't send {answer_substring} anymore")


async def _check_del_media(message: Message, attr: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            if not getattr(user, attr):
                await bot.delete_message(chat_id=message.chat.id,
                                         message_id=message.message_id)


# voice
async def novoice_command(message: Message, session_maker: sessionmaker) -> None:
    await _restrict_media(message, attr='can_send_voice_messages', flag=False,
                          answer_substring='voice', session_maker=session_maker)


async def voiceon_command(message: Message, session_maker: sessionmaker) -> None:
    await _restrict_media(message, attr='can_send_voice_messages',
                          flag=True, session_maker=session_maker)


async def check_voice(message: Message, session_maker: sessionmaker) -> None:
    await _check_del_media(message, 'can_send_voice_messages', session_maker)


# stickers
async def nostickers_command(message: Message, session_maker: sessionmaker) -> None:
    await _restrict_media(message, attr='can_send_stickers', flag=False,
                          answer_substring='stickers', session_maker=session_maker)


async def stickerson_command(message: Message, session_maker: sessionmaker) -> None:
    await _restrict_media(message, attr='can_send_stickers',
                          flag=True, session_maker=session_maker)


async def check_sticker(message: Message, session_maker: sessionmaker) -> None:
    await _check_del_media(message, 'can_send_stickers', session_maker)


# video
async def novideo_command(message: Message, session_maker: sessionmaker) -> None:
    await _restrict_media(message, attr='can_send_video_messages', flag=False,
                          answer_substring='video messages', session_maker=session_maker)


async def videoon_command(message: Message, session_maker: sessionmaker) -> None:
    await _restrict_media(message, attr='can_send_video_messages',
                          flag=True, session_maker=session_maker)


async def check_video(message: Message, session_maker: sessionmaker) -> None:
    await _check_del_media(message, 'can_send_video_messages', session_maker)
