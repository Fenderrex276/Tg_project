import datetime
import uuid

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint
from .keyboards import *
from .states import AdminStates
from .apikeys import api_keys_arr
from db.models import RoundVideo, User, Supt
from .сallbacks import *
from client.initialize import bot as mainbot
from admin.support_reviews.states import ReviewStates


class Admin:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.start_handler, commands=["start"], state='*')
        self.dp.register_message_handler(self.start_handler, text=["start"], state='*')
        self.dp.register_message_handler(self.check_key, state=AdminStates.input_key)
        for i in range(300):
            self.dp.register_message_handler(self.reports, text=f"✅ Репорты ({i})", state="*")
            self.dp.register_message_handler(self.supports, text=f"💚 Поддержка и отзывы ({i})", state="*")

    async def start_handler(self, message: types.Message):
        msg = "Введи свой 🗝 ключ для входа:"
        await self.bot.send_message(message.from_user.id, msg)
        await AdminStates.input_key.set()

    async def check_key(self, message: types.Message, state: FSMContext):
        if message.text in api_keys_arr:
            await self.bot.send_message(message.from_user.id, "Спасибо!")
            await self.bot.send_message(message.from_user.id, "Ключ принят, добро пожаловать!",
                                        reply_markup=types.InlineKeyboardMarkup()
                                        .add(types.InlineKeyboardButton('🔒 Войти', callback_data='enter_bot')
                                             ))
            await state.set_state(AdminStates.is_admin)
        else:
            await self.bot.send_message(message.from_user.id, "Введён неверный ключ")

    async def enter(self, call: types.CallbackQuery, state: FSMContext):
        videos = RoundVideo.objects.exclude(tg_id__isnull=True).filter(status="")
        supports = Supt.objects.filter(solved="new")
        admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

        admin_menu.add(types.KeyboardButton(f"✅ Репорты ({len(videos)})"))
        admin_menu.add(types.KeyboardButton(f"💚 Поддержка и отзывы ({len(supports)})"))

        await self.bot.send_message(call.from_user.id, "Меню админа", reply_markup=admin_menu)
        await call.answer()

    async def reports(self, message: types.Message, state: FSMContext):

        dispute_videos = RoundVideo.objects.exclude(tg_id__isnull=True).filter(
            status="",
            type_video=RoundVideo.TypeVideo.dispute)

        test_videos = RoundVideo.objects.exclude(tg_id__isnull=True).filter(
            status="",
            type_video=RoundVideo.TypeVideo.test)

        reports_menu_keyboard = types.InlineKeyboardMarkup()
        reports_menu_keyboard.add(
            types.InlineKeyboardButton(text=f"Ежедневные ({len(dispute_videos)})", callback_data="every_day"))
        reports_menu_keyboard.add(
            types.InlineKeyboardButton(text=f"Тестовые ({len(test_videos)})", callback_data="test_videos"))
        reports_menu_keyboard.add(types.InlineKeyboardButton(text="До результата (0)", callback_data="before_result"))
        reports_menu_keyboard.add(types.InlineKeyboardButton(text="Архив", callback_data="archive"))

        await message.answer(text="Меню репортов", reply_markup=reports_menu_keyboard)

    async def supports(self, message: types.Message, state: FSMContext):

        await message.answer(text="💚 Поддержка и отзывы", reply_markup=support_menu_keyboard)
        await ReviewStates.none.set()
