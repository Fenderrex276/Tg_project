from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile
from .keyboards import *
from .states import StatesDispute


class CurrentDispute:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.the_hero_path, text=[menu_keyboard, "✅ Путь героя"], state="*")
        self.dp.register_message_handler(self.knowledge_base, text=[menu_keyboard, "💚 База знаний"], state="*")
    async def the_hero_path(self, message: types.Message, state: FSMContext):

        data = await state.get_data()
        purpose = InputFile
        video_with_code = ""
        time_before = "22:30"

        if data['action'] == 'alcohol':
            purpose = InputFile("media/disputs_images/alcohol.jpg")
            video_with_code = "🤳 Видео с кодом и отрицательным алкотестом"

        elif data['action'] == 'smoking':
            purpose = InputFile("media/disputs_images/smoking.jpg")
            video_with_code = "🤳 Видео с кодом и экспресс-тестом"
        elif data['action'] == 'drugs':
            purpose = InputFile("media/disputs_images/drugs.jpg")
            video_with_code = "🤳 Видео с кодом и экспресс-тестом на ПАВ"
        elif data['action'] == "gym":
            purpose = InputFile("media/disputs_images/gym.jpg")
            video_with_code = "🤳 Видео с кодом в зеркале спорт-зала"
        elif data['action'] == "weight":
            purpose = InputFile("media/disputs_images/weight.jpg")
            video_with_code = "🤳 Видео взвешивания с кодом"
        elif data['action'] == "morning":
            if data['additional_action'] == 'five_am':
                time_before = "5:30"
                purpose = InputFile("media/disputs_images/five_am.jpg")
            elif data['additional_action'] == 'six_am':
                time_before = "6:30"
                purpose = InputFile("media/disputs_images/six_am.jpg")
            elif data['additional_action'] == 'seven_am':
                time_before = "7:30"
                purpose = InputFile("media/disputs_images/seven_am.jpg")
            elif data['additional_action'] == 'eight_am':
                time_before = "8:30"
                purpose = InputFile("media/disputs_images/eight_am.jpg")
            video_with_code = "🤳 Видео с кодом в зеркале ванны"
        elif data['action'] == "language":
            if data['additional_action'] == 'english':
                purpose = InputFile("media/disputs_images/english.jpg")
            elif data['additional_action'] == 'chinese':
                purpose = InputFile("media/disputs_images/chinese.jpg")
            elif data['additional_action'] == 'spanish':
                purpose = InputFile("media/disputs_images/spanish.jpg")
            elif data['additional_action'] == 'arabian':
                purpose = InputFile("media/disputs_images/arabian.jpg")
            elif data['additional_action'] == 'italian':
                purpose = InputFile("media/disputs_images/italian.jpg")
            elif data['additional_action'] == 'french':
                purpose = InputFile("media/disputs_images/french.jpg")
            video_with_code = "🤳 Видео с кодом и конспектами"
        elif data['action'] == 'money':
            if data['additional_action'] == 'hundred':
                purpose = InputFile("media/disputs_images/hundred.jpg")
            elif data['additional_action'] == 'three_hundred':
                purpose = InputFile("media/disputs_images/three_hundred.jpg")
            video_with_code = "🤳 Запись экрана из банка с кодом"
        elif data['action'] == 'food':
            purpose = InputFile("media/disputs_images/food.jpg")
            video_with_code = "🤳 Видео с кодом и процессом"
        elif data['action'] == 'programming':
            purpose = InputFile("media/disputs_images/programming.jpg")
            video_with_code = "🤳 Видео с кодом и процессом"
        elif data['action'] == 'instruments':
            if data['additional_action'] == 'piano':
                purpose = InputFile("media/disputs_images/piano.jpg")
            elif data['additional_action'] == 'guitar':
                purpose = InputFile("media/disputs_images/guitar.jpg")
            video_with_code = "🤳 Видео с кодом и процессом"
        elif data['action'] == 'painting':
            purpose = InputFile("media/disputs_images/painting.jpg")
            video_with_code = "🤳 Видео с кодом и процессом"

        start_current_disput_msg = ("*До победы осталось 30 дней*\n\n"
                                    "Условия на 30 дней\n"
                                    f"{video_with_code}\n"
                                    f"⏳ Отправлять в бот до {time_before}\n\n"

                                    f"🧊 Депозит: {data['deposit']} ₽ \n\n")
        await message.answer_photo(photo=purpose)
        await message.answer(text=start_current_disput_msg, reply_markup=report_diary_keyboard,
                             parse_mode=ParseMode.MARKDOWN)

    async def knowledge_base(self, message: types.Message):
        msg = ("*💚 База знаний* \n\n"
               "Читайте о том, как живут и работают самые успешные люди планеты, сохраняйте уникальные мемы,"
               " знакомьтесь с великими книгами и смотрите хорошее кино, чтобы больше узнать о том, "
               "как легче и проще добиваться своих целей, сохранять фокус и мотивацию:")

        await message.answer(text=msg, reply_markup=knowledge_base_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
