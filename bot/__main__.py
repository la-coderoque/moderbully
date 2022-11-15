import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

import bot
import config
from commands import register_common_commands
from commands.base import register_base_commands
from commands.bullying import register_bullying_commands
from commands.moderation import register_moderation_commands
from commands.descriptions import base_cmds
from db import get_async_engine, get_session_maker
from middlewares import register_middlewares


async def main(bot: Bot, dp: Dispatcher) -> None:
    logging.basicConfig(level=logging.INFO)

    await bot.set_my_commands(commands=[BotCommand(command=cmd.command,
                                                   description=cmd.short_desc)
                                        for cmd in base_cmds])
    register_middlewares(dp)
    register_base_commands(dp)
    register_moderation_commands(dp)
    register_bullying_commands(dp)
    register_common_commands(dp)

    async_engine = get_async_engine(config.POSTGRES_URL)
    session_maker = get_session_maker(async_engine)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main(bot.bot, bot.dp))
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
