from aiogram import Router
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.commands.bullying.handlers import check_cursed
from bot.commands.moderation.captcha import check_captcha
from bot.filters import IsGroup


async def check_user(message: Message, session_maker: sessionmaker) -> None:
    await check_captcha(message, session_maker)
    await check_cursed(message, session_maker)


def register_common_commands(router: Router):
    router.message.register(check_user, IsGroup())
