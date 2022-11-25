import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

TOKEN = '5523484221:AAHvprdGu7got6nhM-JDTneBfT1tlcQYR_c'
bot = Bot(TOKEN)
storage = RedisStorage2(host='redis', port=6379, db=3)
dp = Dispatcher(bot, storage=storage)
