from bot.utils.time import DEFAULT_TD
from collections import namedtuple

BASE_PREFIX = '/'
MODER_PREFIX = '!$£'

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
cmd_list_cmd = CmdDesc(['cmd_list'], 'список команд', None, BASE_PREFIX)
base_cmds: list[CmdDesc] = [start_cmd, help_cmd, cmd_list_cmd, whoami_cmd]

# moderation commands
ro_cmd = CmdDesc(
    commands=['ro', 'readonly', 'mute'],
    short_desc='временный read-only',
    long_desc=(
        'Отключает участнику возможность отправлять сообщения в чат, '
        'возможность читать остаётся\n\n'
        f'{REPLY_DESC}\n'
        f'{TD_DESC.format(f"{DEFAULT_TD} минут", "ro", MODER_PREFIX[0])}'
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
        f'{TD_DESC.format("бессрочно", "b", MODER_PREFIX[0])}\n'
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
novoice_cmd = CmdDesc(
    commands=['voice'],
    short_desc='отключает пользователю войсы',
    long_desc=(
        'Отключает участнику возможность отправлять голосовые сообщения в чат\n\n'
        f'{REPLY_DESC}'
    ),
    prefix='-',
)
nostickers_cmd = CmdDesc(
    commands=['stickers'],
    short_desc='отключает пользователю стикеры',
    long_desc=(
        'Отключает участнику возможность отправлять стикеры в чат\n\n'
        f'{REPLY_DESC}'
    ),
    prefix='-',
)
novideo_cmd = CmdDesc(
    commands=['video'],
    short_desc='отключает пользователю видеосообщения',
    long_desc=(
        'Отключает участнику возможность отправлять видеосообщения в чат\n\n'
        f'{REPLY_DESC}'
    ),
    prefix='-',
)
voiceon_cmd = CmdDesc(
    commands=['voice'],
    short_desc='включает пользователю войсы',
    long_desc=(
        'Включает участнику возможность отправлять голосовые сообщения в чат\n\n'
        f'{REPLY_DESC}'
    ),
    prefix='+',
)
stickerson_cmd = CmdDesc(
    commands=['stickers'],
    short_desc='включает пользователю стикеры и гифки',
    long_desc=(
        'Включает участнику возможность отправлять стикеры и гифки в чат\n\n'
        f'{REPLY_DESC}'
    ),
    prefix='+',
)
videoon_cmd = CmdDesc(
    commands=['video'],
    short_desc='включает пользователю видеосообщения',
    long_desc=(
        'Включает участнику возможность отправлять видеосообщения в чат\n\n'
        f'{REPLY_DESC}'
    ),
    prefix='+',
)
is_sheriff_cmd = CmdDesc(
    commands=['is_sheriff', 'issheriff'],
    short_desc='назначает пользователя шерифом',
    long_desc=(
        'Включает участнику возможность использовать модераторские команды, '
        'кроме создания новых шерифов и буллинг-команд\n\n'
        f'{REPLY_DESC}'
    ),
    prefix=MODER_PREFIX,
)
is_not_sheriff_cmd = CmdDesc(
    commands=['is_not_sheriff', 'isnotsheriff'],
    short_desc='снимает пользователя с должности шерифа',
    long_desc=None,
    prefix=MODER_PREFIX,
)
moderation_cmds: list[CmdDesc] = [ro_cmd, rr_cmd, ban_cmd, unmute_cmd,
                                  novoice_cmd, nostickers_cmd, novideo_cmd,
                                  voiceon_cmd, stickerson_cmd, videoon_cmd,
                                  is_sheriff_cmd, is_not_sheriff_cmd]

# bullying commands
cursed_cmd = CmdDesc(
    commands=['curse'],
    short_desc='проклинает пользователя рандомным read-only',
    long_desc=(
        f'Проклятый при отправке каждого сообщения рискует получить <b>{rr_cmd.command}</b> '
        'с вероятностью 2-5% на 1-15 минут\n\n'
        f'{REPLY_DESC}'
    ),
    prefix=MODER_PREFIX,
)
uncursed_cmd = CmdDesc(
    commands=['uncurse'],
    short_desc=f'снимает проклятие <b>{MODER_PREFIX[0]}curse</b>',
    long_desc=None,
    prefix=MODER_PREFIX,
)
despicable_cmd = CmdDesc(
    commands=['despicable', 'презренный'],
    short_desc=f'проклинает восприимчивостью к команде <b>{MODER_PREFIX[0]}shutup</b>',
    long_desc=(
        f'В проклятого каждый может кинуть <b>{MODER_PREFIX[0]}shutup</b> '
        '(ro сработает на 10 минут)\n\n'
        f'{REPLY_DESC}'
    ),
    prefix=MODER_PREFIX,
)
undespicable_cmd = CmdDesc(
    commands=['undespicable', 'непрезренный', 'despicable'],
    short_desc=f'снимает проклятие <b>{MODER_PREFIX[0]}despicable</b>',
    long_desc=None,
    prefix=MODER_PREFIX,
)
shutup_cmd = CmdDesc(
    commands=['shutup', 'завали', 'заткнись'],
    short_desc=f'read-only 10 мин для проклятого <b>{MODER_PREFIX[0]}despicable</b> пользователя',
    long_desc=(
        f'Команда сработает на том, к которому применили <b>{MODER_PREFIX[0]}'
        f'{despicable_cmd.command}\n</b>'
        'Команда сработает от любого участника чата\n\n'
        f'{REPLY_DESC}'
    ),
    prefix=MODER_PREFIX,
)
bullying_cmds: list[CmdDesc] = [cursed_cmd, uncursed_cmd, despicable_cmd,
                                undespicable_cmd, shutup_cmd]
