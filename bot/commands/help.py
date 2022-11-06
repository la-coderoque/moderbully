from aiogram import types
from aiogram.filters import CommandObject

from .descriptions import CMD_DESC


async def help_command(message: types.Message, command: CommandObject):
    if arg := command.args:
        for cmd, _, long_desc in CMD_DESC:
            if cmd == arg:
                if not long_desc:
                    return await message.answer('there is no description for this command')
                return await message.answer(
                    f'{cmd}\n\n{long_desc}'
                )
        else:
            return await message.answer('command not found')

    return await message.answer(
        'use /help <command> to get information about a command'
    )
