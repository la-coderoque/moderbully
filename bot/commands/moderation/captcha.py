from asyncio import sleep
from captcha.image import ImageCaptcha
from random import choice

from aiogram.types import FSInputFile, Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot import bot
from bot.db import User
from bot.commands.common import change_sender_field


SYMBOLS = 'qwertyuiopasdfghjklzxcvbnm'


async def send_captcha(message: Message, session_maker: sessionmaker) -> None:
    chars = ''
    for _ in range(5):
        chars += choice(SYMBOLS)
    image_captcha = ImageCaptcha(width=200, height=200)
    image_captcha.write(chars=chars, output='/tmp/captcha.png')
    image = FSInputFile('/tmp/captcha.png')

    await change_sender_field(message, attr='captcha', value=chars,
                              session_maker=session_maker)

    captcha_msg = await bot.send_photo(chat_id=message.chat.id,
                                       photo=image,
                                       caption='Добро пожаловать '
                                       f'{message.from_user.first_name}!\n'
                                       'Отправь в чат символы с картинки или будешь забанен\n')
    await sleep(60)
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            captcha = getattr(user, 'captcha')
    if captcha:
        await bot.kick_chat_member(chat_id=message.chat.id,
                                   user_id=message.from_user.id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=captcha_msg.message_id)


async def check_captcha(message: Message, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user_id = f'{message.chat.id}_{message.from_user.id}'
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().unique().one_or_none()
            captcha = getattr(user, 'captcha')
    if not captcha:
        return
    if captcha == message.text:
        await change_sender_field(message, attr='captcha', value=None,
                                  session_maker=session_maker)
        allow_msg = await message.answer('Ты доказал что ты не робот, '
                                         f'{message.from_user.first_name}, проходи')
        await sleep(30)
        await bot.delete_message(chat_id=message.chat.id, message_id=allow_msg.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
