from datetime import timedelta

from aiogram.types import ChatPermissions
from bot.utils.time import random_time_in_range, td_format

from . import BaseAction


class RouletteParamsParseError(Exception):
    pass


class ReadOnly(BaseAction):
    async def _get_duration(self) -> timedelta | None:
        return await self._parse_timedelta_from_message()

    async def make(self) -> None:
        if not self.reply_to_user_tg_id:
            return
        elif not (await self.moderator_reply_condition() or await self.sheriff_reply_condition()):
            return
        duration = await self._get_duration()
        if not duration:
            return
        await self.bot.restrict_chat_member(chat_id=self.message.chat.id,
                                            user_id=self.reply_to_user_tg_id,
                                            permissions=ChatPermissions(can_send_messages=False),
                                            until_date=duration)
        await self.message.answer('<b>Read-only</b> activated for user '
                                  f'{self.message.reply_to_message.from_user.first_name}.'
                                  f' Duration: {td_format(duration) or " "}')


class RandomReadOnly(ReadOnly):
    def _random_seconds(self) -> int:
        res = random_time_in_range(0, 24)
        return res if res >= 31 else 31

    async def _get_duration(self) -> timedelta:
        args = getattr(self.command, 'args')
        if not args:
            return timedelta(seconds=self._random_seconds())
        message = self.message
        try:
            cnt, *flg = args.split()
            cnt = int(cnt)
        except (AttributeError, ValueError):
            raise RouletteParamsParseError('Failed to parse cnt from rr params')
        flg += ['max']
        flg = flg[0]
        if flg not in ('min', 'max'):
            raise RouletteParamsParseError('Failed to parse flg from rr params')

        max_spin_cnt = 1000
        min_spin_cnt = 1
        if cnt > max_spin_cnt:
            await message.answer(f'Максимальное количество бросков — {max_spin_cnt}')
            return
        elif cnt < min_spin_cnt:
            await message.answer(f'Минимальное количество бросков — {min_spin_cnt}')
            return

        durations = sorted([self._random_seconds() for _ in range(cnt)])
        min_ = durations[0]
        max_ = durations[-1]
        duration = min_ if flg == 'min' else max_
        await message.answer(f'Кости судьбы были брошены {cnt} '
                             f'раз{"a" if cnt%10>=2 and cnt%10<=4 else ""}\n'
                             f'Минимальное значение: {td_format(timedelta(seconds=min_))}\n'
                             f'Максимальное значение: {td_format(timedelta(seconds=max_))}')
        return timedelta(seconds=duration)


class BanUser(BaseAction):
    async def make(self) -> None:
        if not self.reply_to_user_tg_id:
            return
        elif not (await self.moderator_reply_condition() or await self.sheriff_reply_condition()):
            return
        duration = await self._parse_timedelta_from_message()
        if not duration:
            return
        elif duration.seconds == self._default_td * 60:
            await self.bot.ban_chat_member(
                chat_id=self.message.chat.id,
                user_id=self.reply_to_user_tg_id,
            )
            await self.message.answer(f'User {self.message.reply_to_message.from_user.first_name} '
                                      '<b>banned</b> forever')
        else:
            await self.bot.ban_chat_member(
                chat_id=self.message.chat.id,
                user_id=self.reply_to_user_tg_id,
                until_date=duration,
            )
            await self.message.answer(f'User {self.message.reply_to_message.from_user.first_name} '
                                      f'<b>banned</b> for {td_format(duration) or " "}')
