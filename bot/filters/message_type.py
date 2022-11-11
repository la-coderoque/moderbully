from aiogram.filters import Filter
from aiogram.types import Message


class IsReplyToChannel(Filter):
    async def __call__(self, message: Message) -> None:
        return bool(getattr(message.reply_to_message, 'sender_chat', None))
