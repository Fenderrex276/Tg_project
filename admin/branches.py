from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from .states import AdminStates
from .apikeys import api_keys_arr
from db.models import RoundVideo
from initialize import bot as mainbot
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
        self.dp.register_callback_query_handler(self.access_video, text='good', state="*")
        self.dp.register_callback_query_handler(self.refused_video, text='bad', state="*")

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

    async def reports(self, message: types.Message, state: FSMContext):

        users = RoundVideo.objects.all()
        if len(users) == 0:
            await message.answer("Нет новых видео")
        else:

                id_dispute = str(users[len(users) - 1].user_tg_id)
                disput = id_dispute[5:len(id_dispute)]
                tmp_msg = (f"Диспут #{disput}\n"
                           f"*День 0*\n\n"
                           f"🔒 3 0 2 8\n"
                           f"брошу/начну делать что-то")
                print(users[len(users) - 1].tg_id, "ADMIN BOT")
                await state.update_data(video_user_id=users[len(users) - 1].tg_id)
                await message.answer(text=tmp_msg)

                await message.answer_video_note(video_note=users[len(users) - 1].tg_id,
                                                reply_markup=types.InlineKeyboardMarkup().add(
                                                     types.InlineKeyboardButton(text="⛔️ Не ок", callback_data="bad"),
                                                     types.InlineKeyboardButton(text="👍 Ок", callback_data="good"))
                                                )

    async def access_video(self, call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        RoundVideo.objects.filter(tg_id=data['video_user_id']).update(status="good")
        await call.message.answer(text="Готово")
        user = RoundVideo.objects.get(tg_id=data['video_user_id'])
        success_keyboard = types.InlineKeyboardMarkup()
        success_keyboard.add(types.InlineKeyboardButton(text='👍 Хорошо', callback_data='good'))
        await mainbot.send_message(text="Отлично 🔥 У тебя всё получилось", chat_id=user.chat_tg_id)
        await mainbot.send_message(text="Твой новый код придёт сюда завтра.", chat_id=user.chat_tg_id,
                                   reply_markup=success_keyboard)

    async def refused_video(self, call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        RoundVideo.objects.filter(data['video_user_id']).update(status="bad")
        await call.message.answer(text="Готово")

