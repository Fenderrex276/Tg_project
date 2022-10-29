# from utils import datetime_to_miliseconds
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from branches.dispute_with_friend.messages import dispute_choice_msg
from branches.dispute_with_friend.keyboards import thirty_days_keyboard
from branches.dispute_with_friend.states import Form
from branches.start.keyboards import menu_keyboard
from branches.training.states import Video
from branches.training.keyboards import *


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

    async def recieve_video_note(self, message: types.Message, state: FSMContext):
        file_id = message.video_note.file_id
        print(file_id)
        await state.update_data(video_id=file_id)
        data = await state.get_data()
        print(data)

        tmp_msg = "Пожалуйста, проверь, чётко ли слышен 📣 код на этом видео перед отправкой"
        await message.answer(text=tmp_msg, reply_markup=send_video_keyboard)

    async def recieve_video(self, message: types.Message, state: FSMContext):
        file_id = message.video.file_id

        print(file_id)
        await state.update_data(video_id=file_id)

        tmp_msg = "Пожалуйста, проверь, чётко ли слышен 📣 код на этом видео перед отправкой"
        await message.answer(text=tmp_msg, reply_markup=send_video_keyboard)
