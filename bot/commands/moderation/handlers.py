from aiogram.types import (ChatPermissions, Message)
from datetime import timedelta

from bot import bot
from bot.utils.time import (parse_timedelta_from_message, random_time_in_range,
                            td_format, DEFAULT_TD)
from ..common import apply_restriction, moderator_reply_to_condition


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
    print(random_time_in_range(0, 24))
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
