from datetime import timedelta

from aiogram.types import ChatPermissions
from bot.utils.time import td_format

from . import BaseAction


class ReadOnly(BaseAction):
    async def get_duration(self) -> timedelta | None:
        return await self.parse_timedelta_from_message()

    async def make(self) -> bool:
        if not (await self.moderator_reply_condition() or await self.sheriff_reply_condition()):
            return False
        duration = await self.get_duration()
        if not duration:
            return
        await self.bot.restrict_chat_member(chat_id=self.message.chat.id,
                                            user_id=self.reply_to_user_tg_id,
                                            permissions=ChatPermissions(can_send_messages=False),
                                            until_date=duration)
        await self.message.answer('<b>Read-only</b> activated for user '
                                  f'{self.message.reply_to_message.from_user.first_name}.'
                                  f' Duration: {td_format(duration) or " "}')
