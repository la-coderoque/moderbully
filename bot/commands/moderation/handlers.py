from datetime import timedelta

from aiogram.filters import CommandObject
from aiogram.types import ChatPermissions, Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot import bot
from bot.db import User
from bot.utils.time import (parse_timedelta_from_message, random_time_in_range,
                            td_format, DEFAULT_TD)
from ..common import (apply_restriction, change_reply_to_user_field,
                      moderator_reply_to_condition, sheriff_reply_to_condition)


class RouletteParamsParseError(Exception):
    pass


# read only
async def read_only_command(message: Message, command: CommandObject,
                            session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    duration = await parse_timedelta_from_message(message)
    if not duration:
        return
    await apply_restriction(message=message,
                            permissions=ChatPermissions(can_send_messages=False),
                            duration=duration)


async def random_read_only_command(message: Message, command: CommandObject,
                                   session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
        return
    duration = random_time_in_range(0, 24)
    if args := command.args:
        try:
            cnt, *flg = args.split()
            cnt = int(cnt)
        except (AttributeError, ValueError):
            raise RouletteParamsParseError('Failed to parse cnt from rr params')
        flg += ['max']
        flg = flg[0]
        if flg not in ('min', 'max'):
            raise RouletteParamsParseError('Failed to parse flg from rr params')

        max_spin_cnt = 1000
        min_spin_cnt = 1
        if cnt > max_spin_cnt:
            await message.answer(f'Максимальное количество бросков — {max_spin_cnt}')
            return
        elif cnt < min_spin_cnt:
            await message.answer(f'Минимальное количество бросков — {min_spin_cnt}')
            return

        durations = sorted([random_time_in_range(0, 24) for _ in range(cnt)])
        min_ = durations[0]
        max_ = durations[-1]
        duration = min_ if flg == 'min' else max_
        await message.answer(f'Кости судьбы были брошены {cnt} '
                             f'раз{"a" if cnt%10>=2 and cnt%10<=4 else ""}\n'
                             f'Минимальное значение: {td_format(timedelta(seconds=min_))}\n'
                             f'Максимальное значение: {td_format(timedelta(seconds=max_))}')
    await apply_restriction(message=message,
                            permissions=ChatPermissions(can_send_messages=False),
                            duration=timedelta(seconds=duration))


# ban
async def ban_command(message: Message, session_maker: sessionmaker) -> None:
    if not (await moderator_reply_to_condition(message) or
            await sheriff_reply_to_condition(message, session_maker)):
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
