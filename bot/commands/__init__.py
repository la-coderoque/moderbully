from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandStart

from commands.help import help_command
from commands.start import start_command
from commands.whoami import whoami_callback, whoami_command, WhoCallbackData


def register_user_commands(router: Router) -> None:
    router.message.register(start_command, CommandStart())

    router.message.register(help_command, Command(commands=['help']))

    router.message.register(whoami_command, Command(commands=['whoami']))
    router.callback_query.register(whoami_callback, WhoCallbackData.filter())
