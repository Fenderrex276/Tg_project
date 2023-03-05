
from aiogram.types import InputFile

from aiogram.utils.markdown import link

from .keyboards import *

test_alcohol_link = link("Например", "https://www.ozon.ru/category/alkotestery-6256/")
alcohol_msg = ("*🍷 Брошу пить алкоголь*\n\n"
               "Для этой цели надобится самостоятельно"
               f"приобрести любой цифровой алкотестер. {test_alcohol_link}")

test_smoke_link = link("Например", "https://www.ozon.ru/search/?from_global=true&text=%D0%A2%D0%95%D0%A1%D0%A2+%D0%9A%D0%9E%D0%A2%D0%98%D0%9D%D0%98%D0%9D")
smoking_msg = ("*🚬 Брошу курить никотин*\n\n"
               "Для этой цели понадобится самостоятельно приобрести экспресс-тесты (30 шт на 30 дней)"
               f"на котинин. {test_smoke_link}")

test_pav_link = link("Например", "https://www.ozon.ru/category/test-na-narkotiki-35150/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D0%A2%D0%95%D0%A1%D0%A2+%D0%BC%D0%B0%D1%80%D0%B8%D1%85%D1%83%D0%B0%D0%BD%D0%B0")
drugs_msg = ("*💊 Брошу употреблять ПАВ\n\n*"
             "Для этой цели понадобится самостоятельно приобрести экспресс-тесты (30 шт на 30 дней)"
             f" на вид/ы ПАВ. {test_pav_link}")

gymm_msg = ("*💪 Буду ходить в спорт-зал\n\n*"
            "Для этой цели понадобится актуальный абонемент в фитнес-клуб на 1 месяц."
            " Без абонемента эта цель недоступна.")

weight_msg = ("*🌱 Похудею на 5 кг\n\n*"
              "Не важно, теряешь ли ты вес каждый день или нет. Важно соблюдать условия Диспута, и к концу"
              " 30 дня быть легче первоначального веса на 5 кг, даже если получится достичь результата раньше.")

morning_msg = "*🌤 Буду вставать рано утром\n*"

language_msg = "*🇬🇧 Буду учить иностранный язык\n\n*"

money_msg = "*💰Накоплю или отложу за 30 дней*"
money_msg2 = ("Создай отдельный накопительный счёт в любом банке, "
              "чтобы сделать запись экрана истории пополнений, даже если пополнений в "
              "этот день не было.")

healthy_food_msg = ("*🍏 Научусь готовить здоровую еду*\n\n"
                    "Не важно получается ли что-то каждый день или нет. Важно соблюдать условия "
                    "Диспута и показывать процесс 30 дней.\n "
                    "🌤 Ежедневная работа даёт результат абсолютно в любом деле.")

programming_msg = ("*💻 Научусь программировать*\n\n"
                   "Не важно получается ли что-то каждый день или нет. Важно соблюдать условия "
                   "Диспута и показывать процесс 30 дней.\n "
                   "🌤 Ежедневная работа даёт результат абсолютно в любом деле.")

instruments_msg = "*🎼 Научусь играть на...\n\n*"

instruments_msg2 = ("Не важно получается ли что-то каждый день или нет. Важно соблюдать условия "
                    "Диспута и показывать процесс 30 дней.\n "
                    "🌤 Ежедневная работа даёт результат абсолютно в любом деле.")

painting_msg = "*🎨 Научусь рисовать...\n\n*"

painting_msg2 = ("Не важно получается ли что-то каждый день или нет. Важно соблюдать условия "
                 "Диспута и показывать процесс 30 дней.\n "
                 "🌤 Ежедневная работа даёт результат абсолютно в любом деле.")

monday_or_later_msg = ("Диспут продлится каждый из 30 последующих дней, без возможности прерваться."
                       " Когда ты готов/а начать?")

promo_code_msg = ("🎟 Введи сюда промо-код и получи право на одну ошибку без потери депозита.\n"
                  "Если промо-кода нет, нажми на кнопку ниже")

geo_position_msg = ("🌍 Укажи разницу во времени относительно UTC (Москва +3, Красноярск +7 и тд) или отправь в бот "
                    "геопозицию (возьмем только часовой пояс)")

confirm_alcohol_disput_msg = ("*Условия пари на 30 дней*\n"
                              "🤳 Видео с кодом и отрицательным алкотестом\n"
                              "⌛ Отправлять в бот до 22:30\n\n")

second_msg = (f"Каждый день бот заранее присылает уведомление со специальным"
              f" кодом из четырех цифр, который тебе необходимо произнести на "
              f"видео, как в примере, и отправить в бот вовремя\.\n\n"
              f"👍Если всё ок, игра продолжится и вы сохраните свой депозит\n\n"
              f"👎Если правила игры нарушены, вы проиграете сначала 20% депозита, "
              f"а если это повторится — остальные 80%\.")

confirm_smoking_disput_msg = ("*Условия пари на 30 дней*\n"
                              "🤳 Видео с кодом и экспресс\-тестом на котинин\n"
                              "⌛ Отправлять в бот до 22:30\n\n")

confirm_drugs_disput_msg = ("*Условия пари на 30 дней*\n"
                            "🤳 Видео с кодом и экспресс\-тестом на необходимые ПАВ\n"
                            "⌛ Отправлять в бот до 22:30\n\n")

confirm_gym_disput_msg = ("*Условия пари на 30 дней*\n"
                          "🤳 Видео с кодом в зеркале спорт\-зала\n"
                          "⌛ Отправлять в бот до 22:30\n\n")

confirm_weight_disput_msg = ("*Условия пари на 30 дней*\n"
                             "🤳 Видео взвешивания с кодом\n"
                             "⌛ Отправлять в бот до 22:30\n\n")

confirm_morning_disput_msg = ("*Условия пари на 30 дней*\n"
                              "🤳 Видео с кодом в зеркале ванны\n")

confirm_language_disput_msg = ("*Условия пари на 30 дней*\n"
                               "🤳 Видео с кодом и конспектами\n"
                               "⌛ Отправлять в бот до 22:30\n\n")

confirm_money_disput_msg = ("*Условия пари на 30 дней*\n"
                            "🤳 Запись экрана из банка\n"
                            "⌛ Отправлять в бот до 22:30\n\n")

confirm_food_disput_msg = ("*Условия пари на 30 дней*\n"
                           "🤳 Видео с кодом и процессом\n"
                           "⌛ Отправлять в бот до 22:30\n\n")

confirm_programming_disput_msg = ("*Условия пари на 30 дней*\n"
                                  "🤳 Видео с кодом и процессом\n"
                                  "⌛ Отправлять в бот до 22:30\n\n")

months = {"January": "Января", "February": "Февраля", "March": "Марта", "April": "Апреля", "May": "Мая", "June": "Июня",
          "July": "Июля", "August": "Августа", "September": "Сентября", "October": "Октября",
          "November": "Ноября", "December": "Декабря"}


def get_timezone_msg(future_date, variant, ):
    date_start = str(future_date.day) + " " + months[str(future_date.strftime('%B'))] + " " + str(future_date.year)

    choice_msg = ""
    tmp_keyboard = types.InlineKeyboardMarkup
    photo = InputFile

    promocode = variant['promocode']
    if promocode != '0':
        promocode = '1'

    if variant['action'] == 'alcohol':
        photo = InputFile("client/media/disputs_images/alcohol.jpg")
        choice_msg = f'{confirm_alcohol_disput_msg}Начало 🚩{date_start} \nПраво на ошибку:' \
                     f' {promocode}\n\n{second_msg} '
        tmp_keyboard = alcohol_deposit_keyboard

    elif variant['action'] == 'smoking':
        photo = InputFile("client/media/disputs_images/smoking.jpg")
        choice_msg = f'{confirm_smoking_disput_msg}Начало 🚩{date_start} \nПраво на ошибку:' \
                     f' {promocode}\n\n{second_msg} '
        tmp_keyboard = smoking_deposit_keyboard

    elif variant['action'] == 'drugs':
        photo = InputFile("client/media/disputs_images/drugs.jpg")
        choice_msg = f'{confirm_drugs_disput_msg}Начало 🚩{date_start} \nПраво на ошибку:' \
                     f' {promocode}\n\n{second_msg}'
        tmp_keyboard = drugs_deposit_keyboard

    elif variant['action'] == 'gym':
        photo = InputFile("client/media/disputs_images/gym.jpg")
        choice_msg = f'{confirm_gym_disput_msg}Начало 🚩{date_start} \nПраво на ошибку:' \
                     f' {promocode}\n\n{second_msg}'
        tmp_keyboard = gym_deposit_keyboard

    elif variant['action'] == 'weight':
        photo = InputFile("client/media/disputs_images/weight.jpg")
        choice_msg = f'{confirm_weight_disput_msg}Начало 🚩{date_start} \nПраво на ошибку:' \
                     f' {promocode}\n\n{second_msg}'
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

        choice_msg = f'{confirm_morning_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
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
        choice_msg = f'{confirm_language_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = language_deposit_keyboard

    elif variant['action'] == 'money':
        if variant['additional_action'] == 'hundred':
            photo = InputFile("client/media/disputs_images/hundred.jpg")
        elif variant['additional_action'] == 'three_hundred':
            photo = InputFile("client/media/disputs_images/three_hundred.jpg")
        choice_msg = f'{confirm_money_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = money_deposit_keyboard

    elif variant['action'] == 'food':
        photo = InputFile("client/media/disputs_images/food.jpg")
        choice_msg = f'{confirm_food_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = food_deposit_keyboard

    elif variant['action'] == 'programming':
        photo = InputFile("client/media/disputs_images/programming.jpg")
        choice_msg = f'{confirm_programming_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = programming_deposit_keyboard

    elif variant['action'] == 'instruments':
        if variant['additional_action'] == 'piano':
            photo = InputFile("client/media/disputs_images/piano.jpg")
        elif variant['additional_action'] == 'guitar':
            photo = InputFile("client/media/disputs_images/guitar.jpg")
        choice_msg = f'{confirm_programming_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = instruments_deposit_keyboard

    elif variant['action'] == 'painting':
        photo = InputFile("client/media/disputs_images/painting.jpg")
        choice_msg = f'{confirm_programming_disput_msg}Начало 🚩{date_start}' \
                     f' \nПраво на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = painting_deposit_keyboard

    return photo, choice_msg, tmp_keyboard
