from aiogram import types
from aiogram.filters import CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.commands.descriptions import base_cmds, moderation_cmds, bullying_cmds
import config

CMDS = base_cmds + moderation_cmds + bullying_cmds


class WhoCallbackData(CallbackData, prefix='who'):
    user_id: int


async def start_command(message: types.Message) -> None:
    await message.answer(
        f'Привет, {message.from_user.first_name}!\n'
        'Я — бот, предназначенный для модерирования чатов\nЧтобы '
        'использовать мой функционал — добавь меня в групповой чат и выдай мне '
        'админские права\n'
        'Отправь <b>/cmd_list</b>, чтобы получить список моих команд\n'
        'Отправь <b>/help</b>, чтобы узнать, как пользоваться командами',
    )


async def help_command(message: types.Message, command: CommandObject) -> None:
    if arg := command.args:
        for cmd in CMDS:
            if cmd.command == arg:
                res = f'<b>{cmd.prefix[0]}{cmd.command} — {cmd.short_desc}</b>'
                aliases = ''
                for alias in cmd.aliases:
                    aliases += f'<b>{cmd.prefix[0]}{alias}</b>\n'
                if cmd.long_desc:
                    res += f'\n\n{cmd.long_desc}'
                if aliases:
                    res += '\n\nПсевдонимы/ссылки/синонимы:\n'
                    res += aliases[:-1:]
                if not cmd.long_desc and not aliases:
                    return await message.answer('Для этой команды нет подробного описания')
                return await message.answer(res)
        else:
            return await message.answer('Команда не найдена')

    await message.answer(
        'Напиши <b>/help <i>название_команды_без_префикса</i></b> чтобы получить о ней справку\n'
        'Например: <b>/help help</b>'
    )


async def cmd_list_command(message: types.Message) -> None:
    res = ''
    for cmd in CMDS:
        res += f'<b>{cmd.prefix[0]}{cmd.command}</b> — {cmd.short_desc}\n'
    return await message.answer(res[:-1:])


async def whoami_command(message: types.Message) -> None:
    whoami_markup = InlineKeyboardBuilder()
    whoami_markup.button(
        text='yeah',
        callback_data=WhoCallbackData(
            user_id=message.from_user.id,
        )
    )
    await message.answer('do you want to know your id?', reply_markup=whoami_markup.as_markup())


async def whoami_callback(call: types.CallbackQuery, callback_data: WhoCallbackData) -> None:
    ans = f'{str(callback_data.user_id)}'
    if callback_data.user_id in config.ADMIN_ID:
        ans = f'Hi chief!\n\nYour id: {ans}'
    await call.message.answer(ans)
