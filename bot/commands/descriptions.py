from bot.utils.time import DEFAULT_TD
from collections import namedtuple

BASE_PREFIX = '/'
MODER_PREFIX = '!'

REPLY_DESC = 'Срабатывает при ответе командой на сообщение пользователя в групповом чате'
TD_DESC = (
    'Параметром передаётся продолжительность действия\n'
    'При отсутствии параметра — {0}\n\n'
    'Примеры использования:\n'
    '{2}{1} 2w — две недели\n'
    '{2}{1} 10d — десять дней\n'
    '{2}{1} 5h — пять часов\n'
    '{2}{1} 120m — сто двадцать минут\n'
    '{2}{1} 666s — шестьсот шестьдесят шесть секунд'
)


class CmdDesc(namedtuple('CmdDesc', 'commands, short_desc, long_desc, prefix')):
    @property
    def command(self) -> str:
        return self[0][0]

    @property
    def aliases(self) -> list:
        return self[0][1:]


# base commands
start_cmd = CmdDesc(['start'], 'запустить справку о боте', None, BASE_PREFIX)
help_cmd = CmdDesc(
    commands=['help'],
    short_desc='путеводитель',
    long_desc=(
        'Если ты читаешь это сообщение — ты умеешь пользоваться командой <b>/help</b> 🤩\n\n'
        '<b>/cmd_list</b> — список всех команд'
    ),
    prefix=BASE_PREFIX,
)
whoami_cmd = CmdDesc(['whoami'], 'получить айди своего тг-аккаунта', None, BASE_PREFIX)
cmd_list_cmd = CmdDesc(
    commands=['cmd_list'],
    short_desc='список команд',
    long_desc=(
        'команды делятся на несколько типов, для наглядности они отличаются префиксами:\n'
        '<b>/</b> — справочные команды 📖\n'
        '<b>!</b> — модераторские команды 🗝️\n'
        '<b>%</b> — \n'
        '<b>&</b> — \n'
    ),
    prefix=BASE_PREFIX,
)
base_cmds: list[CmdDesc] = [start_cmd, help_cmd, cmd_list_cmd, whoami_cmd]

# moderation commands
ro_cmd = CmdDesc(
    commands=['ro', 'readonly', 'mute', 'shutup', 'fuckoff', 'помолчи'],
    short_desc='временный read-only',
    long_desc=(
        'Отключает участнику возможность отправлять сообщения в чат, '
        'возможность читать остаётся\n\n'
        f'{REPLY_DESC}\n'
        f'{TD_DESC.format(f"{DEFAULT_TD} минут", "ro", MODER_PREFIX)}'
    ),
    prefix=MODER_PREFIX,
)
rr_cmd = CmdDesc(
    commands=['rr', 'roulette', 'кк'],
    short_desc='случайный read-only',
    long_desc=(
        'Отключает участнику возможность отправлять сообщения в чат '
        'на случайный промежуток времени (не более суток), возможность читать остаётся\n\n'
        f'{REPLY_DESC}'
    ),
    prefix=MODER_PREFIX,
)
ban_cmd = CmdDesc(
    commands=['b', 'ban'],
    short_desc='бан',
    long_desc=(
        'Удаляет пользователя из чата, запрещает вступать в чат\n'
        f'{REPLY_DESC}\n'
        f'{TD_DESC.format("бессрочно", "b", MODER_PREFIX)}\n'
        'При применении команды в ответ на сообщение отправленное от имени канала '
        'бан для канала будет бессрочным'
    ),
    prefix=MODER_PREFIX,
)
unmute_cmd = CmdDesc(
    commands=['u', 'unmute', 'unban'],
    short_desc='разбан',
    long_desc=(
        'Разбанивает пользователей и каналы, снимает read-only\n\n'
        f'{REPLY_DESC}'
    ),
    prefix=MODER_PREFIX,
)
moderation_cmds: list[CmdDesc] = [ro_cmd, rr_cmd, ban_cmd, unmute_cmd]
