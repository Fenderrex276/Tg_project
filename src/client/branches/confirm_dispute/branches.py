from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, InputFile

from client.branches.confirm_dispute.keyboards import instruments_deposit_keyboard, painting_deposit_keyboard
from client.branches.start.keyboards import menu_keyboard
from client.branches.confirm_dispute.states import Promo
from client.branches.confirm_dispute.keyboards import *
from client.branches.confirm_dispute.mesages import *
from utils import get_timezone, get_date_to_start_dispute
from db.models import User

class ConfirmDispute:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.input_promo_code_handler, state=Promo.input_promo)
        self.dp.register_message_handler(self.get_geo_position, content_types=['location'], state=Promo.geo_position)

    async def input_promo_code_handler(self, message: types.Message, state: FSMContext):
        promocodes = ['HUI', 'ZALUPA', 'CHLEN', 'PIDARAS', 'SOBCHAK']

        print(message.text)
        # TODO проходимся по базе и ищем промокоды среди зарегистрированных пользоватей
        #  ищем по полю promocode_user если находим то добавляем этот промокод в поле
        #  promocode_from_user текущего пользователя, но сначала храним его в редисе
        if message.text in promocodes or User.objects.filter(promocode_user=message.text).exists():
            msg = 'Спасибо 🙏 Промо-код успешно принят.'
            await Promo.next()
            await state.update_data(promocode=message.text)
            await message.answer(text=msg)
            await message.answer(text=geo_position_msg, reply_markup=choose_time_zone_keyboard)

        else:
            msg = 'Неверный промокод, попробуйте ещё раз'
            await message.answer(text=msg)

    async def get_geo_position(self, message: types.Message, state: FSMContext):

        loc = message.location
        # print(loc)
        tmp = get_timezone(loc)
        await state.update_data(timezone=tmp[:len(tmp) - 4])
        msg = f"Установлен часовой пояс {tmp}"

        await message.answer(text=msg)

        variant = await state.get_data()

        print(message.date)
        future_date = get_date_to_start_dispute(message.date, variant['start_disput'], tmp[:len(tmp) - 4])
        date_start = str(future_date.day) + " " + str(future_date.strftime('%B')) + " " + str(future_date.year)

        choice_msg = ""
        tmp_keyboard = types.InlineKeyboardMarkup
        photo = InputFile

        promocode = variant['promocode']
        if promocode != '0':
            promocode = '1'

        if variant['action'] == 'alcohol':
            photo = InputFile("client/media/disputs_images/alcohol.jpg")
            choice_msg = f'{confirm_alcohol_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = alcohol_deposit_keyboard

        elif variant['action'] == 'smoking':
            photo = InputFile("client/media/disputs_images/smoking.jpg")
            choice_msg = f'{confirm_smoking_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = smoking_deposit_keyboard

        elif variant['action'] == 'drugs':
            photo = InputFile("client/media/disputs_images/drugs.jpg")
            choice_msg = f'{confirm_drugs_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = drugs_deposit_keyboard

        elif variant['action'] == 'gym':
            photo = InputFile("client/media/disputs_images/gym.jpg")
            choice_msg = f'{confirm_gym_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = gym_deposit_keyboard

        elif variant['action'] == 'weight':
            photo = InputFile("client/media/disputs_images/weight.jpg")
            choice_msg = f'{confirm_weight_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = weight_deposit_keyboard

        elif variant['action'] == 'morning':
            if variant['additional_action'] == 'five_am':
                photo = InputFile("client/media/disputs_images/five_am.jpg")
            elif variant['additional_action'] == 'six_am':
                photo = InputFile("client/media/disputs_images/six_am.jpg")
            elif variant['additional_action'] == 'seven_am':
                photo = InputFile("client/media/disputs_images/seven_am.jpg")
            elif variant['additional_action'] == 'eight_am':
                photo = InputFile("client/media/disputs_images/eight_am.jpg")

            choice_msg = f'{confirm_morning_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = morning_deposit_keyboard

        elif variant['action'] == 'language':
            if variant['additional_action'] == 'english':
                photo = InputFile("client/media/disputs_images/english.jpg")
            elif variant['additional_action'] == 'chinese':
                photo = InputFile("client/media/disputs_images/chinese.jpg")
            elif variant['additional_action'] == 'spanish':
                photo = InputFile("client/media/disputs_images/spanish.jpg")
            elif variant['additional_action'] == 'arabian':
                photo = InputFile("client/media/disputs_images/arabian.jpg")
            elif variant['additional_action'] == 'italian':
                photo = InputFile("client/media/disputs_images/italian.jpg")
            elif variant['additional_action'] == 'french':
                photo = InputFile("client/media/disputs_images/french.jpg")
            choice_msg = f'{confirm_language_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = language_deposit_keyboard

        elif variant['action'] == 'money':
            if variant['additional_action'] == 'hundred':
                photo = InputFile("client/media/disputs_images/hundred.jpg")
            elif variant['additional_action'] == 'three_hundred':
                photo = InputFile("client/media/disputs_images/three_hundred.jpg")
            choice_msg = f'{confirm_money_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = money_deposit_keyboard

        elif variant['action'] == 'food':
            photo = InputFile("client/media/disputs_images/food.jpg")
            choice_msg = f'{confirm_food_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = food_deposit_keyboard

        elif variant['action'] == 'programming':
            photo = InputFile("client/media/disputs_images/programming.jpg")
            choice_msg = f'{confirm_programming_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = programming_deposit_keyboard

        elif variant['action'] == 'instruments':
            if variant['additional_action'] == 'piano':
                photo = InputFile("client/media/disputs_images/piano.jpg")
            elif variant['additional_action'] == 'guitar':
                photo = InputFile("client/media/disputs_images/guitar.jpg")
            choice_msg = f'{confirm_programming_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = instruments_deposit_keyboard

        elif variant['action'] == 'painting':
            photo = InputFile("client/media/disputs_images/painting.jpg")
            choice_msg = f'{confirm_programming_disput_msg}Начало 🚩{date_start} \nПраво на ошибку: {promocode}\n\n{second_msg}'
            tmp_keyboard = painting_deposit_keyboard

        await message.answer_photo(photo=photo, caption=choice_msg, reply_markup=tmp_keyboard,
                                   parse_mode=ParseMode.MARKDOWN_V2)
#        await message.answer(text=choice_msg, reply_markup=tmp_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
        await state.update_data({'id_to_delete': message.message_id + 1}) # ??????? пофиксить
        await Promo.next()
