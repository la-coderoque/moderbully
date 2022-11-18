from aiogram.filters import CommandObject
from aiogram.types import ChatPermissions, Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot import bot
from bot.actions.moderation import BanUser, RandomReadOnly, ReadOnly
from bot.db import User
from bot.utils.time import (parse_timedelta_from_message, td_format, DEFAULT_TD)
from ..common import (apply_restriction, change_reply_to_user_field,
                      moderator_reply_to_condition, sheriff_reply_to_condition)


class RouletteParamsParseError(Exception):
    pass


# read only
async def read_only_command(message: Message, command: CommandObject,
                            session_maker: sessionmaker) -> None:
    await ReadOnly(bot, message, session_maker, command).make()


async def random_read_only_command(message: Message, command: CommandObject,
                                   session_maker: sessionmaker) -> None:
    await RandomReadOnly(bot, message, session_maker, command).make()


# ban
async def ban_command(message: Message, command: CommandObject,
                      session_maker: sessionmaker) -> None:
    await BanUser(bot, message, session_maker, command).make()


async def ban_sender_chat_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await bot.ban_chat_sender_chat(chat_id=message.chat.id,
                                   sender_chat_id=message.reply_to_message.sender_chat.id)
    await message.answer(f'Channel {message.reply_to_message.sender_chat.title} '
                         '<b>banned</b> forever')


# unmute|unban
async def unmute_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        only_if_banned=True,
    )
    await apply_restriction(message=message,
                            permissions=ChatPermissions(can_send_messages=True,
                                                        can_send_media_messages=True,
                                                        can_send_other_messages=True,
                                                        can_send_polls=True,
                                                        can_add_web_page_previews=True,
                                                        can_change_info=True,
                                                        can_invite_users=True,
                                                        can_pin_messages=True))
    await message.answer(f'User {message.reply_to_message.from_user.first_name} unrestricted')


async def unban_sender_chat_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await bot.unban_chat_sender_chat(chat_id=message.chat.id,
                                     sender_chat_id=message.reply_to_message.sender_chat.id)
    await message.answer(f'Channel {message.reply_to_message.sender_chat.title} <b>unbanned</b>')


# media
async def _check_del_media(message: Message, attr: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            if not getattr(user, attr):
                await bot.delete_message(chat_id=message.chat.id,
                                         message_id=message.message_id)


async def _media_restrict_answer(message: Message, answer_substring: str, restrict: bool) -> None:
    if restrict:
        await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                             f"can't send {answer_substring} anymore")
    else:
        await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                             f"can send {answer_substring} now")


# voice
async def novoice_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await change_reply_to_user_field(message, attr='can_send_voice_messages', flag=False,
                                     session_maker=session_maker)
    await _media_restrict_answer(message, 'voice', True)


async def voiceon_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await change_reply_to_user_field(message, attr='can_send_voice_messages',
                                     flag=True, session_maker=session_maker)
    await _media_restrict_answer(message, 'voice', False)


async def check_voice(message: Message, session_maker: sessionmaker) -> None:
    await _check_del_media(message, 'can_send_voice_messages', session_maker)


# stickers
async def nostickers_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await change_reply_to_user_field(message, attr='can_send_stickers', flag=False,
                                     session_maker=session_maker)
    await _media_restrict_answer(message, 'stickers', True)


async def stickerson_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await change_reply_to_user_field(message, attr='can_send_stickers',
                                     flag=True, session_maker=session_maker)
    await _media_restrict_answer(message, 'stickers', False)


async def check_sticker(message: Message, session_maker: sessionmaker) -> None:
    await _check_del_media(message, 'can_send_stickers', session_maker)


# video
async def novideo_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await change_reply_to_user_field(message, attr='can_send_video_messages', flag=False,
                                     session_maker=session_maker)
    await _media_restrict_answer(message, 'video messages', True)


async def videoon_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    await change_reply_to_user_field(message, attr='can_send_video_messages',
                                     flag=True, session_maker=session_maker)
    await _media_restrict_answer(message, 'video messages', False)


async def check_video(message: Message, session_maker: sessionmaker) -> None:
    await _check_del_media(message, 'can_send_video_messages', session_maker)


# sheriff
async def is_sheriff_command(message: Message, session_maker: sessionmaker) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await change_reply_to_user_field(message, attr='is_sheriff',
                                     flag=True, session_maker=session_maker)
    await message.answer(f'User {message.reply_to_message.from_user.first_name} is sheriff now')


async def is_not_sheriff_command(message: Message, session_maker: sessionmaker) -> None:
    if not await moderator_reply_to_condition(message):
        return
    await change_reply_to_user_field(message, attr='is_sheriff',
                                     flag=False, session_maker=session_maker)
    await message.answer(f'User {message.reply_to_message.from_user.first_name} '
                         'is not sheriff now')
