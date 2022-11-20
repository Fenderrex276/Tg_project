from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from admin.reports.callbacks import test_videos
from admin.сallbacks import current_dispute
from db.models import RoundVideo, Users
from initialize import bot as mainbot
from admin.reports.states import ReportStates


class Reports:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.input_message, state=ReportStates.input_message)
        self.dp.register_message_handler(self.input_id_dispute, state=ReportStates.input_id_dispute)
        self.dp.register_message_handler(self.input_number_of_day, state=ReportStates.input_number_day)

    async def input_message(self, message: types.Message, state: FSMContext):
        v = await state.get_data()
        RoundVideo.objects.filter(tg_id=v['video_user_id']).update(status="bad",
                                                                   type_video=RoundVideo.TypeVideo.archive)
        user = RoundVideo.objects.get(tg_id=v['video_user_id'])

        await mainbot.send_message(text=message.text,
                                   chat_id=user.chat_tg_id,
                                   reply_markup=types.InlineKeyboardMarkup().add(
                                       types.InlineKeyboardButton(text='Отправить репорт', callback_data="send_new1")
                                   ))
        await ReportStates.none.set()
        await message.answer("Готово!")

    async def input_id_dispute(self, message: types.Message, state: FSMContext):
        id_dispute = int(message.text[2:])
        dispute_videos = RoundVideo.objects.filter(id_video=id_dispute)
        tmp_msg = ""
        if len(dispute_videos) == 0:
            tmp_msg = "Диспут не найден.\nСкопируй номер диспута и введи (#D****):"
        else:
            await ReportStates.input_number_day.set()
            await state.update_data(id_archive=id_dispute)
            tmp_msg = "Введи день"

        await message.answer(text=tmp_msg)

    async def input_number_of_day(self, message: types.Message, state: FSMContext):

        tmp_msg = ""
        if message.text.isdigit():
            n_day = int(message.text)
            data = await state.get_data()
            dispute_video = RoundVideo.objects.filter(id_video=data['id_archive'], n_day=n_day).first()
            if dispute_video is None:
                tmp_msg = "Такого видео нет, попробуйте выбрать другой день"
                await message.answer(text=tmp_msg)
            else:
                await ReportStates.none.set()
                user = Users.objects.filter(user_id=dispute_video.user_tg_id).first()
                code_in_video = " ".join(list(dispute_video.code_in_video))
                description_dispute = current_dispute(user.action, user.additional_action)
                answer_admin = ""

                if dispute_video.status == RoundVideo.VideoStatus.good:
                    answer_admin = "👍 Ок"
                elif dispute_video.status == RoundVideo.VideoStatus.bad:
                    answer_admin = "⛔️ Не ок"

                tmp_msg = (f"Диспут #D{data['id_archive']}\n"
                           f"День {n_day}\n\n"
                           f"🔒 {code_in_video}\n"
                           f"{description_dispute}\n\n"
                           f"{answer_admin}")
                print(user.action)
                print(dispute_video.tg_id)
                if user.action == "money":
                    await message.answer_video(video=dispute_video.tg_id)
                else:
                    await message.answer_video_note(video_note=dispute_video.tg_id)
                await message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(text='Ещё', callback_data='more_video')
                ))
        else:
            tmp_msg = "Неккоректный номер дня, попробуйте ещё раз"

            await message.answer(text=tmp_msg)


