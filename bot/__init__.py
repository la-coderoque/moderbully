from aiogram import Bot, Dispatcher

from bot import config

bot = Bot(config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()
