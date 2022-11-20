from aiogram import Bot, Dispatcher

from .keyboards import *
from .states import AdminStates
from .apikeys import api_keys_arr
from .сallbacks import *


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
        self.dp.register_callback_query_handler(self.enter, text='enter_bot', state="*")
        self.dp.register_message_handler(self.reports, text="✅ Репорты", state="*")

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
            await AdminStates.is_admin.set()
        else:
            await self.bot.send_message(message.from_user.id, "Введён неверный ключ")

    async def enter(self, call: types.CallbackQuery, state: FSMContext):
        await call.message.answer("Меню админа", reply_markup=admin_menu)

    async def reports(self, message: types.Message, state: FSMContext):

        await message.answer(text="Меню репортов", reply_markup=reports_menu_keyboard)


