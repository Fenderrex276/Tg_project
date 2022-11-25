from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = ['5646356632:AAFmwBQuf7V91t--qGoJS4tcAdCCpNI8PAo']
bot = Bot(TOKEN[0])
storage = RedisStorage2(host='redis', port=6379, db=10)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()
