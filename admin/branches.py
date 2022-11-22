import datetime
import uuid

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint
from .keyboards import *
from .states import AdminStates
from .apikeys import api_keys_arr
from db.models import RoundVideo, Users
from .сallbacks import *
from initialize import bot as mainbot
from initialize import scheduler
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
        self.dp.register_callback_query_handler(self.enter, text='enter_bot')
        self.dp.register_message_handler(self.reports, text="✅ Репорты", state="*")
        self.dp.register_message_handler(self.supports, text="💚 Поддержка и отзывы", state="*")

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
        await self.bot.send_message(call.from_user.id, "Меню админа", reply_markup=admin_menu)

    async def reports(self, message: types.Message, state: FSMContext):

        await message.answer(text="Меню репортов", reply_markup=reports_menu_keyboard)

    async def supports(self, message: types.Message, state: FSMContext):

        await message.answer(text="💚 Поддержка и отзывы", reply_markup=support_menu_keyboard)
        await ReviewStates.none.set()


