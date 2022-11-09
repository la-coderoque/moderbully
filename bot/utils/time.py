import datetime
from random import choices, randint
import re
import typing

from aiogram import types

PATTERN = re.compile(r"(?P<value>\d+)(?P<modifier>[wdhms])")
LINE_PATTERN = re.compile(r"^(\d+[wdhms]){1,}$")
DEFAULT_TD = 15  # minutes

MODIFIERS = {
    "w": datetime.timedelta(weeks=1),
    "d": datetime.timedelta(days=1),
    "h": datetime.timedelta(hours=1),
    "m": datetime.timedelta(minutes=1),
    "s": datetime.timedelta(seconds=1),
}


class TimedeltaParseError(Exception):
    pass


def parse_timedelta(value: str) -> datetime.timedelta:
    match = LINE_PATTERN.match(value)
    if not match:
        raise TimedeltaParseError('Invalid time format')

    try:
        result = datetime.timedelta()
        for match in PATTERN.finditer(value):
            value, modifier = match.groups()

            result += int(value) * MODIFIERS[modifier]
    except OverflowError:
        raise TimedeltaParseError('Timedelta value is too large')
    except (KeyError, ValueError):
        raise TimedeltaParseError('Wrong format')

    return result


async def parse_timedelta_from_message(
    message: types.Message,
) -> typing.Optional[datetime.timedelta]:
    _, *args = message.text.split()

    if args:  # Parse custom duration
        try:
            duration = parse_timedelta(args[0])
        except TimedeltaParseError:
            await message.reply('Failed to parse duration')
            return
        if duration <= datetime.timedelta(seconds=30):
            return datetime.timedelta(seconds=30)
        return duration

    return datetime.timedelta(minutes=DEFAULT_TD)


def td_format(td_object: datetime.timedelta) -> str | None:
    if not isinstance(td_object, datetime.timedelta):
        return
    seconds = int(td_object.total_seconds())
    periods = [
        ('yr', 60*60*24*365),
        ('mo', 60*60*24*30),
        ('d',  60*60*24),
        ('h',  60*60),
        ('m',  60),
        ('s',  1),
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            strings.append('%s%s' % (period_value, period_name))

    return ', '.join(strings)


def random_time_in_range(start: int, stop: int) -> int:
    other_weights = 21 * [0.02]
    rand_seconds = choices(range(start, stop),
                           weights=[0.1, 0.38, 0.1, *other_weights])
    rand_seconds = rand_seconds[0] * 3600 + randint(0, 3600)
    return rand_seconds
