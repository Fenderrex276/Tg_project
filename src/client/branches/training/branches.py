# from utils import datetime_to_miliseconds
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from client.branches.training.states import Video
from client.branches.training.keyboards import *


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

    async def recieve_video_note(self, message: types.Message, state: FSMContext):
        file_id = message.video_note.file_id
        await state.update_data(video_id=file_id)

        tmp_msg = "Пожалуйста, проверь, чётко ли слышен 📣 код на этом видео перед отправкой"
        await message.answer(text=tmp_msg, reply_markup=send_video_keyboard)

    async def recieve_video(self, message: types.Message, state: FSMContext):
        file_id = message.video.file_id

        await state.update_data(video_id=file_id)

        tmp_msg = "Пожалуйста, проверь, чётко ли слышен 📣 код на этом видео перед отправкой"
        await message.answer(text=tmp_msg, reply_markup=send_video_keyboard)

    async def is_not_a_video(self, message: types.Message):
        error_message = "Ошибка. Мы принимаем репорт только в видео-формате."
        await message.answer(text=error_message, reply_markup=send_help_keyboard)

