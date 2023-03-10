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

    async def demo_hero_path(self, message: types.Message, state: FSMContext):
        try:
            user_video = await RoundVideo.objects.filter(user_tg_id=message.from_user.id,
                                                         chat_tg_id=message.chat.id,
                                                         type_video=RoundVideo.TypeVideo.test
                                                         ).alast()

            # user_video = await RoundVideo.objects.aget(id_video=data['id_video_code'])
            if user_video.status == "" and user_video.tg_id is not None:
                tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."
                await message.answer(text=tmp_msg)
            else:
                await message.answer(text=pin_chat_msg, reply_markup=success_keyboard)
        except RoundVideo.DoesNotExist:

            purpose = ""
            video_with_code = ""
            time_before = "22:30"
            data = await state.get_data()

            if data['action'] == 'alcohol':
                purpose = "🍷 Брошу пить алкоголь"
                video_with_code = "🤳 Видео с кодом и отрицательным алкотестом"

            elif data['action'] == 'smoking':
                purpose = "🚬 Брошу курить никотин"
                video_with_code = "🤳 Видео с кодом и экспресс-тестом"
            elif data['action'] == 'drugs':
                purpose = "💊 Брошу употреблять ПАВ"
                video_with_code = "🤳 Видео с кодом и экспресс-тестом на ПАВ"
            elif data['action'] == "gym":
                purpose = "💪 Буду ходить в спорт-зал"
                video_with_code = "🤳 Видео с кодом в зеркале спорт-зала"
            elif data['action'] == "weight":
                purpose = "🌱 Похудею на 5 кг"
                video_with_code = "🤳 Видео взвешивания с кодом"
            elif data['action'] == "morning":
                if data['additional_action'] == 'five_am':
                    time_before = "5:30"
                    purpose = "🌤 Буду вставать в 5 утра"
                elif data['additional_action'] == 'six_am':
                    time_before = "6:30"
                    purpose = "🌤 Буду вставать в 6 утра"
                elif data['additional_action'] == 'seven_am':
                    time_before = "7:30"
                    purpose = "🌤 Буду вставать в 7 утра"
                elif data['additional_action'] == 'eight_am':
                    time_before = "8:30"
                    purpose = "🌤 Буду вставать в 8 утра"
                video_with_code = "🤳 Видео с кодом в зеркале ванны"
            elif data['action'] == "language":
                if data['additional_action'] == 'english':
                    purpose = "🇬🇧 Буду учить английский язык"
                elif data['additional_action'] == 'chinese':
                    purpose = "🇬🇧 Буду учить китайский язык"
                elif data['additional_action'] == 'spanish':
                    purpose = "🇬🇧 Буду учить испанский язык"
                elif data['additional_action'] == 'arabian':
                    purpose = "🇬🇧 Буду учить арабский язык"
                elif data['additional_action'] == 'italian':
                    purpose = "🇬🇧 Буду учить итальянский язык"
                elif data['additional_action'] == 'french':
                    purpose = "🇬🇧 Буду учить французский язык"
                video_with_code = "🤳 Видео с кодом и конспектами"
            elif data['action'] == 'money':
                if data['additional_action'] == 'hundred':
                    purpose = "💰Накоплю 100 000 ₽"
                elif data['additional_action'] == 'three_hundred':
                    purpose = "💰Накоплю 300 000 ₽"
                video_with_code = "🤳 Запись экрана из банка с кодом"
            elif data['action'] == 'food':
                purpose = "🍏 Научусь готовить здоровую еду"
                video_with_code = "🤳 Видео с кодом и процессом"
            elif data['action'] == 'programming':
                purpose = "💻 Научусь программировать"
                video_with_code = "🤳 Видео с кодом и процессом"
            elif data['action'] == 'instruments':
                if data['additional_action'] == 'piano':
                    purpose = "🎼 Научусь играть на фортепиано"
                elif data['additional_action'] == 'guitar':
                    purpose = "🎼 Научусь играть на гитаре"
                video_with_code = "🤳 Видео с кодом и процессом"
            elif data['action'] == 'painting':
                purpose = "🎨 Научусь рисовать"
                video_with_code = "🤳 Видео с кодом и процессом"
            promo = data['promocode']
            if promo != '0':
                promo = '1'
            start_current_disput_msg = (f"👋 Привет, {data['user_name']},"
                                        f" заверши свою подготовку к цели и начни путь героя.\n\n"
                                        "*Твоя цель:*\n"
                                        f"{purpose}\n"
                                        f"🧊 Депозит: {data['deposit']} ₽ \n\n"
                                        "*Условия на 30 дней*\n"
                                        f"{video_with_code}\n"
                                        f"⏳ Отправлять в бот до {time_before}\n\n"
                                        "До победы осталось 30 дней\n"
                                        f"Право на ошибку: {promo}")

            await message.answer(text=start_current_disput_msg,
                                 parse_mode=ParseMode.MARKDOWN, reply_markup=next_step_keyboard)

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
