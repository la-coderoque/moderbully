from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder
)

import config


class WhoCallbackData(CallbackData, prefix='who'):
    user_id: int
    is_bot_admin: bool = False


async def whoami_command(message: types.Message):
    whoami_markup = InlineKeyboardBuilder()
    whoami_markup.button(
        text='yeah',
        callback_data=WhoCallbackData(
            user_id=message.from_user.id,
        )
    )
    await message.answer('do you want to know your id?', reply_markup=whoami_markup.as_markup())


async def whoami_callback(call: types.CallbackQuery, callback_data: WhoCallbackData):
    ans = f'{str(callback_data.user_id)}'
    if callback_data.user_id in config.ADMIN_IDS:
        ans = f'Hi chief!\n\nYour id: {ans}'

    await call.message.answer(ans)
