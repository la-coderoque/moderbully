from aiogram import Router
from aiogram.filters import Command

from bot.commands.descriptions import BULLY_PREFIX, cursed_cmd, uncursed_cmd
from bot.filters import IsGroup
from .handlers import check_user_state, cursed_command, uncursed_command


def register_bullying_commands(router: Router):
    for command, cmd in ((cursed_command, cursed_cmd),
                         (uncursed_command, uncursed_cmd)):
        router.message.register(command, IsGroup(),
                                Command(commands=cmd.commands, prefix=BULLY_PREFIX))
    router.message.register(check_user_state, IsGroup())
