import datetime

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
        self.dp.register_callback_query_handler(self.test_videos, text='test_videos', state="*")
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
        await self.bot.send_message(call.from_user.id, "Меню админа", reply_markup=admin_menu)

    async def reports(self, message: types.Message, state: FSMContext):

        await message.answer(text="Меню репортов", reply_markup=reports_menu_keyboard)

    async def test_videos(self, call: types.CallbackQuery, state: FSMContext):

        new_videos = RoundVideo.objects.filter(status="").first()

        if new_videos is None:
            await call.message.answer("Нет новых видео")
        else:
            user = Users.objects.filter(user_id=new_videos.user_tg_id).first()
            id_dispute = str(new_videos.id_video)
            purpose = current_dispute(user.action, user.additional_action)

            code = " ".join(list(new_videos.code_in_video))

            tmp_msg = (f"Диспут \#D{id_dispute}\n"
                       f"*День 0*\n\n"
                       f"🔒 {code}\n"
                       f"{purpose}")
            # print(new_videos.tg_id, "ADMIN BOT")

            await state.update_data(video_user_id=new_videos.tg_id)
            await call.message.answer(text=tmp_msg, parse_mode=ParseMode.MARKDOWN_V2)
            if user.action == "money":
                await call.message.answer_video(video=new_videos.tg_id,
                                                reply_markup=test_keyboard)
            else:
                await call.message.answer_video_note(video_note=new_videos.tg_id,
                                                     reply_markup=test_keyboard)

    async def access_video(self, call: types.CallbackQuery, state: FSMContext):

        data = await state.get_data()
        RoundVideo.objects.filter(tg_id=data['video_user_id']).update(status="good")
        await call.message.answer(text="Готово")
        user = RoundVideo.objects.get(tg_id=data['video_user_id'])
        current_user = Users.objects.filter(user_id=user.user_tg_id).first()
        start = ""

        if current_user.start_disput == "tomorrow":
            start = "Послезавтра"
        elif current_user.start_disput == "monday":
            start = "в понедельник"
        success_keyboard = types.InlineKeyboardMarkup()
        success_keyboard.add(types.InlineKeyboardButton(text='👍 Хорошо', callback_data='good'))

        await mainbot.send_message(text="Отлично 🔥 У тебя всё получилось", chat_id=user.chat_tg_id)
        await mainbot.send_message(text=f"Твой новый код придёт сюда {start}.", chat_id=user.chat_tg_id,
                                   reply_markup=success_keyboard)
        date_now = call.message.date + datetime.timedelta(minutes=1)
        scheduler.start()
        scheduler.add_job(self.new_code, "date", run_date=date_now, args=(user.chat_tg_id,))
        scheduler.print_jobs()

    async def refused_video(self, call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        RoundVideo.objects.filter(data['video_user_id']).update(status="bad")
        await call.message.answer(text="Готово")

    async def new_code(self, chat_id: int):
        new_code = str(randint(1000, 9999))
        msg = f"Твой новый код: {new_code}"
        await mainbot.send_message(text=msg, chat_id=chat_id)
