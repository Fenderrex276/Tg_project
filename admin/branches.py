from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from .states import AdminStates
from .apikeys import api_keys_arr


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
            await state.finish()
        else:
            await self.bot.send_message(message.from_user.id, "Введён неверный ключ")

    async def enter(self, call: types.CallbackQuery, state: FSMContext):
        await self.bot.send_message(call.from_user.id, "Меню админа", reply_markup=types.ReplyKeyboardMarkup(
            [[types.KeyboardButton("✅ Репорты")], [types.KeyboardButton("💚 Поддержка и отзывы")]], resize_keyboard=True
        ))
