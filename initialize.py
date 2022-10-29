from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

TOKEN = '5646356632:AAFmwBQuf7V91t--qGoJS4tcAdCCpNI8PAo'
bot = Bot(TOKEN)
storage = RedisStorage2(host='localhost', port=6379, db=2)
dp = Dispatcher(bot, storage=storage)

