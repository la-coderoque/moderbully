from typing import Optional

from aiogram.types import (ChatMember, ChatMemberAdministrator,
                           ChatMemberOwner, ChatPermissions, Message)
from datetime import timedelta

from bot import bot
from bot.utils.time import td_format


# await bot.get_chat_administrators(chat_id=message.chat.id)
def list_admin_ids(admins: list[ChatMemberAdministrator, ChatMemberOwner]) -> list[int]:
    return [admin.user.id for admin in admins if not admin.user.is_bot]


def can_user_restrict_other(user_1: ChatMember, user_2: ChatMember) -> bool:
    """
    can user_1 restrict user_2?
    """
    statuses = ('creator', 'administrator')
    return user_1.status in statuses and user_2.status not in statuses


async def moderator_reply_to_condition(message: Message) -> bool:
    sender: ChatMember = await bot.get_chat_member(chat_id=message.chat.id,
                                                   user_id=message.from_user.id)
    reply_to_user: ChatMember = await bot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
    ) if message.reply_to_message else None
    if reply_to_user and can_user_restrict_other(sender, reply_to_user):
        return True


async def apply_restriction(message: Message, permissions: ChatPermissions,
                            duration: Optional[timedelta] = None):
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=permissions,
        until_date=duration,
    )

    if not permissions.can_send_messages:
        await message.answer(
            '<b>Read-only</b> activated for user '
            f'{message.reply_to_message.from_user.first_name}.'
            f' Duration: {td_format(duration) or " "}',
        )
