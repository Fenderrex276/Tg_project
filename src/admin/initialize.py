import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from settings.settings import TOKEN_ADMIN, REDIS_PASSWORD

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

TOKEN = TOKEN_ADMIN
bot = Bot(TOKEN)
storage = RedisStorage2(host='redis', port=6379, db=3, password=REDIS_PASSWORD)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone=utc)
