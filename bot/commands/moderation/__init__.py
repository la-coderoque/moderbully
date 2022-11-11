from aiogram import F, Router
from aiogram.filters import Command

from bot.commands.descriptions import (ban_cmd, is_sheriff_cmd, is_not_sheriff_cmd, MODER_PREFIX,
                                       nostickers_cmd, novideo_cmd, novoice_cmd, ro_cmd, rr_cmd,
                                       stickerson_cmd, videoon_cmd, voiceon_cmd, unmute_cmd)
from bot.filters import IsReplyToChannel, IsGroup
from .handlers import (ban_command, ban_sender_chat_command,
                       check_sticker, check_video, check_voice, is_sheriff_command,
                       is_not_sheriff_command, nostickers_command,
                       novideo_command, novoice_command, read_only_command,
                       random_read_only_command, stickerson_command, videoon_command,
                       voiceon_command, unban_sender_chat_command, unmute_command)


def register_moderation_commands(router: Router) -> None:
    for command, cmd in ((ban_sender_chat_command, ban_cmd),
                         (unban_sender_chat_command, unmute_cmd)):
        router.message.register(command, IsReplyToChannel(),
                                Command(commands=cmd.commands, prefix=MODER_PREFIX))
    for command, cmd in ((read_only_command, ro_cmd),
                         (random_read_only_command, rr_cmd),
                         (ban_command, ban_cmd),
                         (unmute_command, unmute_cmd),
                         (novoice_command, novoice_cmd),
                         (voiceon_command, voiceon_cmd),
                         (nostickers_command, nostickers_cmd),
                         (stickerson_command, stickerson_cmd),
                         (novideo_command, novideo_cmd),
                         (videoon_command, videoon_cmd),
                         (is_sheriff_command, is_sheriff_cmd),
                         (is_not_sheriff_command, is_not_sheriff_cmd)):
        router.message.register(command, IsGroup(),
                                Command(commands=cmd.commands, prefix=MODER_PREFIX))
    router.message.register(check_voice, IsGroup(), F.voice)
    router.message.register(check_sticker, IsGroup(), F.sticker)
    router.message.register(check_video, IsGroup(), F.video_note)
