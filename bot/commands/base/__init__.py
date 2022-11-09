from aiogram import Router
from aiogram.filters import Command

from bot.commands.descriptions import cmd_list_cmd, help_cmd, start_cmd, whoami_cmd
from bot.filters import IsPrivate
from .handlers import (cmd_list_command, help_command, start_command,
                       whoami_callback, whoami_command, WhoCallbackData)


def register_base_commands(router: Router) -> None:
    for command, cmd in ((start_command, start_cmd),
                         (help_command, help_cmd),
                         (whoami_command, whoami_cmd),
                         (cmd_list_command, cmd_list_cmd)):
        router.message.register(command, IsPrivate(),
                                Command(commands=cmd.commands, prefix=cmd.prefix))
    router.callback_query.register(whoami_callback, WhoCallbackData.filter())
