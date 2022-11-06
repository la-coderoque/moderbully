import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

import config
from commands import register_user_commands
from commands.descriptions import CMD_DESC
from db import get_async_engine, get_session_maker


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()

    commands = [
        BotCommand(command=cmd, description=inline_desc)
        for cmd, inline_desc, _ in CMD_DESC
    ]
    await bot.set_my_commands(commands=commands)
    register_user_commands(dp)

    async_engine = get_async_engine(config.POSTGRES_URL)
    session_maker = get_session_maker(async_engine)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
