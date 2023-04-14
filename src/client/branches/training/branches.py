# from utils import datetime_to_miliseconds
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from client.branches.pay.keyboards import next_step_keyboard
from client.branches.thirty_days_dispute.keyboards import menu_keyboard
from client.branches.training.messages import pin_chat_msg
from client.branches.training.states import Video
from client.branches.training.keyboards import *
from db.models import User, Supt, RoundVideo
from client.branches.pay.callbacks import start_current_disput
from client.branches.pay.states import PayStates

class Training:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        # команды
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.recieve_video_note, content_types=['video_note'],
                                         state=Video.recv_video_note)
        self.dp.register_message_handler(self.recieve_video, content_types=['video'], state=Video.recv_video)
        self.dp.register_message_handler(self.is_not_a_video,
                                         content_types=['text', 'audio', 'photo', 'sticker', 'voice'],
                                         state=Video.recv_video)
        self.dp.register_message_handler(self.is_not_a_video,
                                         content_types=['text', 'audio', 'photo', 'sticker', 'voice', 'video'],
                                         state=Video.recv_video_note)

        self.dp.register_message_handler(self.input_support, state=Video.new_question)

        # self.dp.register_message_handler(self.demo_hero_path, text=["✅ Путь героя"], state=PayStates.all_states)
    async def recieve_video_note(self, message: types.Message, state: FSMContext):
        file_id = message.video_note.file_id
        await state.update_data(video_id=file_id)

        tmp_msg = "Пожалуйста, проверь, чётко ли видим 📣 код на этом видео перед отправкой"
        await message.answer(text=tmp_msg, reply_markup=send_video_keyboard)

    async def recieve_video(self, message: types.Message, state: FSMContext):
        file_id = message.video.file_id

        await state.update_data(video_id=file_id)

        tmp_msg = "Пожалуйста, проверь, чётко ли видим 📣 код на этом видео перед отправкой"
        await message.answer(text=tmp_msg, reply_markup=send_video_keyboard)

    async def is_not_a_video(self, message: types.Message):
        error_message = "Ошибка. Мы принимаем репорт только в видео-формате."
        await message.answer(text=error_message, reply_markup=send_help_keyboard)

    async def input_support(self, message: types.Message, state: FSMContext):

        try:
            nd = await User.objects.filter(user_id=message.from_user.id).alast()
            n = nd.number_dispute
        except:
            n = 0
        await Supt.objects.acreate(user_id=message.from_user.id,
                                   number_dispute=n,
                                   chat_id=message.chat.id,
                                   problem=message.text,
                                   solved=Supt.TypeSolve.new)

        data = await state.get_data()
        if data['action'] == 'money':
            await Video.recv_video.set()
        else:
            await Video.recv_video_note.set()

        await message.answer(text='Готово! 🤗 Спасибо')
