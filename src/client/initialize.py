from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = ['5119201221:AAEwngH-vR4R07oLxav__mbxrR3MQq-CF68', '5721619250:AAEM7EoCMFrSg2VKwU5FiAzkhQ-FCUUxBsw']
bot = Bot(TOKEN[0])
storage = RedisStorage2(host='redis', port=6379, db=10)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()
