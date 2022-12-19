import datetime
import random

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile
from aiogram.utils.markdown import link
from asgiref.sync import sync_to_async

from utils import get_timezone
from .diary import questions
from .keyboards import *
from .states import StatesDispute, NewReview
from .callbacks import video_text
from db.models import Supt, User, Reviews, RoundVideo
import pytz
from .callbacks import random_question


class CurrentDispute:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.the_hero_path, text=[menu_keyboard, "✅ Путь героя"],
                                         state=StatesDispute.all_states)
        self.dp.register_message_handler(self.knowledge_base, text=[menu_keyboard, "💚 База знаний"],
                                         state="*")
        self.dp.register_message_handler(self.account, text=[menu_keyboard, "🟢 Аккаунт"],
                                         state="*")

        self.dp.register_message_handler(self.process_name_invalid, lambda message: len(message.text) > 20,
                                         state=StatesDispute.change_name)

        self.dp.register_message_handler(self.input_name, state=StatesDispute.change_name)
        self.dp.register_message_handler(self.recieve_video_note, content_types=['video_note'],
                                         state=StatesDispute.video_note)
        self.dp.register_message_handler(self.recieve_video, content_types=['video'], state=StatesDispute.video_note)
        self.dp.register_message_handler(self.is_not_a_video,
                                         content_types=['text', 'audio', 'photo', 'sticker', 'voice'],
                                         state=StatesDispute.video)
        self.dp.register_message_handler(self.is_not_a_video,
                                         content_types=['text', 'audio', 'photo', 'sticker', 'voice'],
                                         state=StatesDispute.video_note)
        self.dp.register_message_handler(self.inpute_answer, state=StatesDispute.diary)
        self.dp.register_message_handler(self.input_support, state=StatesDispute.new_question)
        self.dp.register_message_handler(self.new_timezone, content_types=['location'],
                                         state=StatesDispute.new_timezone)
        self.dp.register_message_handler(self.input_city, state=NewReview.input_city)
        self.dp.register_message_handler(self.get_coment, state=NewReview.input_review)

    async def the_hero_path(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        print(current_state)
#        await StatesDispute.none.set()
        if current_state in StatesDispute.states_names:
            await StatesDispute.none.set()
            print(current_state)
        else:
            return

        """user = await User.objects.filter(user_id=message.from_user.id).alast()
        await state.update_data(action=user.action,
                                additional_action=user.additional_action,
                                start_disput=user.start_disput,
                                promocode=user.promocode_from_friend,
                                timezone=user.timezone,
                                name=user.user_name,
                                deposit=user.deposit,
                                id_dispute=user.number_dispute)
        """
        data = await state.get_data()
        print(data)
        user = await User.objects.filter(user_id=message.from_user.id).alast()
        count_days = user.count_days

        recieve_message = video_text(data, count_days)
        print('HEROPATH, ', message.message_id)
        await message.answer_photo(photo=InputFile(recieve_message[0]),
                                   caption=recieve_message[1],
                                   reply_markup=report_diary_keyboard,
                                   parse_mode=ParseMode.MARKDOWN)

    async def knowledge_base(self, message: types.Message):
        await StatesDispute.knowledge_base.set()
        msg = ("*💚 База знаний* \n\n"
               "Читайте о том, как живут и работают самые успешные люди планеты, сохраняйте уникальные мемы,"
               " знакомьтесь с великими книгами и смотрите хорошее кино, чтобы больше узнать о том, "
               "как легче и проще добиваться своих целей, сохранять фокус и мотивацию:")

        await message.answer(text=msg, reply_markup=knowledge_base_keyboard, parse_mode=ParseMode.MARKDOWN_V2)

    async def account(self, message: types.Message, state: FSMContext):
        await StatesDispute.account.set()
        user = await state.get_data()
        msg = (f"👋 *Привет, {user['name']}* \n\n"
               "Здесь ты можешь изменить своё имя, вывести выигранный депозит, "
               "изменить свой часовой пояс или написать свой вопрос в тех. "
               "поддержку через форму обратной связи.")

        await message.answer(text=msg, reply_markup=account_keyboard, parse_mode=ParseMode.MARKDOWN)

    async def new_timezone(self, message: types.Message, state: FSMContext):
        loc = message.location
        # print(loc)
        tmp = get_timezone(loc)
        await state.update_data(timezone=tmp[:len(tmp) - 4])
        user = await User.objects.filter(user_id=message.from_user.id).alast()
        user.timezone = tmp[:len(tmp) - 4]
        user.save()
        msg = f"Установлен часовой пояс {tmp}"
        await StatesDispute.none.set()
        await message.answer(text=msg, reply_markup=menu_keyboard)

    async def input_name(self, message: types.Message, state: FSMContext):
        await StatesDispute.account.set()
        await state.update_data(name=message.text)
        user = await User.objects.filter(user_id=message.from_user.id).alast()
        user.user_name = message.text
        user.save()
        await message.answer(text='Готово!')

    async def process_name_invalid(self, message: types.Message):
        msg = "Максимум 20 символов, пожалуйста попробуйте ещё раз"
        return await message.answer(msg)

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
        await message.answer(text=error_message)

    async def inpute_answer(self, message: types.Message, state: FSMContext):
        print(message.text)

        await message.answer('Готово!')
        number = await state.get_data()
        ind = number['number_question']
        second_ind = random.randint(0, 29)
        if second_ind == ind:
            second_ind = random.randint(0, 29)
        await state.update_data(number_question=second_ind)
        await message.answer(text=questions[second_ind], reply_markup=admit_or_pass_keyboard)

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
        await StatesDispute.none.set()
        await message.answer(text='Готово! 🤗 Спасибо')

    async def input_city(self, message: types.Message, state: FSMContext):

        await NewReview.none.set()
        await state.update_data(city_for_review=message.text)
        await message.answer(text="🎲 Оцени игру и твой личный опыт взаимодействия с ботом:", reply_markup=mark_keyboard)

    async def get_coment(self, message: types.Message, state: FSMContext):
        user = await User.objects.filter(user_id=message.from_user.id).alast()
        current_video = await RoundVideo.objects.filter(user_tg_id=message.from_user.id,
                                                        type_video=RoundVideo.TypeVideo.archive).alast()
        data = await state.get_data()
        await NewReview.none.set()
        await Reviews.objects.acreate(user_id=message.from_user.id,
                                      chat_id=message.chat.id,
                                      user_name=user.user_name,
                                      id_dispute=current_video.id_video,
                                      city=data['city_for_review'],
                                      mark=data['stars'],
                                      coment=message.text,
                                      state_t=Reviews.StateReview.new
                                      )

        await message.answer(text="Готово! Спасибо за отзыв ❤️", reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='Спорим 🤝 ещё', callback_data='new_dispute')))

