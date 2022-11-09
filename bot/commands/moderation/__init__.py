from aiogram import Router
from aiogram.filters import Command

from bot.commands.descriptions import (ban_cmd, MODER_PREFIX, ro_cmd,
                                       rr_cmd, unmute_cmd)
from bot.filters import IsGroup
from .handlers import (ban_command, read_only_command, random_read_only_command,
                       unmute_command)


def register_moderation_commands(router: Router) -> None:
    for command, cmd in ((read_only_command, ro_cmd),
                         (random_read_only_command, rr_cmd),
                         (ban_command, ban_cmd),
                         (unmute_command, unmute_cmd)):
        router.message.register(command, IsGroup(),
                                Command(commands=cmd.commands, prefix=MODER_PREFIX))
