from aiogram.types import InputFile

from aiogram.utils.markdown import link, escape_md
from .keyboards import *

test_alcohol_link = link("Например такие, если вы хотите бросить пить алкоголь.",
                         "https://ozon.ru/t/3aPZXA3")
alcohol_msg = ("*🍷 Брошу пить алкоголь*\n\n"
               "Для этой цели понадобится самостоятельно приобрести экспресс\-тесты \(30 шт на 30 дней\) на "
               "алкоголь\.\n\n"
               f"{test_alcohol_link}\n\n"
               f"⚠\! Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать "
               f"прогресс "
               f" не смогут быть выполнены\.")

test_smoke_link = link("Например такие, если вы хотите бросить курить никотин.",
                       "https://ozon.ru/t/gGzr1R8")
smoking_msg = ("*🚬 Брошу курить никотин*\n\n"
               "Для этой цели понадобится самостоятельно приобрести экспресс\-тесты \(30 шт на 30 дней\) на котинин\.\n\n"
               f"{test_smoke_link}\n\n⚠ Без самостоятельной покупки тестов спор будет проигран, "
               f"так как ваши обязательства доказать прогресс не смогут быть выполнены\.")

test_pav_link = link("экспресc-тесты (30 шт на 30 дней)",
                     "https://domtest.su/catalog/testy_na_narkotiki_/")
test_pav_link2 = link("Например такие, если вы хотите бросить употреблять марихуану.",
                      "https://ozon.ru/t/n4pNn8N")
drugs_msg = ("*💊 Брошу употреблять ПАВ\n\n*"
             f"Для этой цели понадобится самостоятельно приобрести {test_pav_link}\.\n\n"
             f"{test_pav_link2}\n\n"
             "⚠ Без самостоятельной покупки тестов спор будет проигран, "
             "так как ваши обязательства доказать прогресс не смогут быть выполнены\.")

gymm_msg = ("*💪 Буду ходить в спорт-зал\n\n*"
            "Для этой цели понадобится самостоятельно приобрести абонемент в фитнес-клуб на 1 месяц.\n\n"
            "⚠ Без абонемента спор будет проигран, так как ваши обязательства доказать прогресс"
            " не смогут быть выполнены. В случаях, если ваш зал не будет работать в выходные и праздники - ваша задача "
            "попасть в другой зал или на спорт-площадку.")

weight_msg = ("*🌱 Похудею на 5 кг\n\n*"
              "Для этой цели понадобится ежедневно взвешиваться на исправных электронных весах.\n\n"
              "⚠ Не важно, теряешь ли ты вес каждый день или нет. Важно к концу 30 дня быть легче первоначального "
              "веса на 5 кг, даже если получится достичь результата раньше. Можно снимать себя без лица, "
              "главное, чтобы на видео был четко слышен уникальный код и вы отправляли его вовремя.")

morning_msg = "*🌤 Буду вставать рано утром\n*"

language_msg = "*🇬🇧 Буду учить иностранный язык\n\n*"

money_msg = "*💰Накоплю или отложу за 30 дней*"
money_msg2 = ("Создай отдельный накопительный счёт в любом банке, "
              "чтобы сделать запись экрана истории пополнений, даже если пополнений в "
              "этот день не было.")

healthy_food_msg = ("*🍏 Научусь готовить здоровую еду*\n\n"
                    "Для этой цели понадобится самостоятельно ежедневно готовить здоровую еду.\n\n"

                    "⚠ Принимаются видео только с процессом приготовления еды, а не с готовым блюдом. "
                    "На видео обязательно должен быть четко слышен код.")

programming_msg = ("*💻 Научусь программировать*\n\n"
                   "Для этой цели понадобится самостоятельно ежедневно программировать.\n\n"
                   "⚠ Принимаются видео только с процессом программирования. "
                   "На видео обязательно должен быть четко слышен код.")

instruments_msg = "*🎼 Научусь играть на...\n\n*"

# instruments_msg2 = ("Не важно получается ли что-то каждый день или нет. Важно соблюдать условия "
#                     "Диспута и показывать процесс 30 дней.\n "
#                     "🌤 Ежедневная работа даёт результат абсолютно в любом деле.")


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
without_msg = ("Диспут продлится каждый из 30 последующих дней, без возможности прерваться. Дату начала ты сможешь "
               "выбрать после прохождения подготовки.")

confirm_morning_msg = (
    "Для этой цели понадобится ежедневно просыпаться рано утром и делать короткое видео в зеркале ванны.\n\n"
    "⚠ Можно снимать себя без лица, главное, чтобы на видео был четко слышен уникальный код и вы отправляли"
    " его вовремя.")

confirm_language_msg = (
    "Для этой цели понадобится ежедневно уделять время изучению языка."
    " Учить новые слова и делать конспекты упражнений.\n\n"
    "⚠ Постарайтесь делать записи новых слов или правил в отдельную тетрадь. Без письменных свидетельств учебы "
    "спор будет проигран, так как ваши обязательства доказать прогресс не смогут быть выполнены, "
    "если вы занимаетесь исключительно на сайте или в приложениях. На видео обязательно должен "
    "быть слышен код.")

confirm_money_msg = ("Для этой цели понадобится создать накопительный счёт в приложении любого банка, "
                     "чтобы ежедневно делать видео-запись экрана истории пополнений, даже если пополнений в этот день"
                     " не было.\n\n"
                     "⚠ Важно к концу 30 дня иметь на счету загаданную сумму, даже если получится достичь результата"
                     " раньше. На каждой записи экрана обязательно должен быть четко виден ваш код, "
                     "который приходит каждое утро.")

confirm_music_msg = ("Для этой цели понадобится самостоятельно ежедневно играть на музыкальном инструменте.\n\n"
                     "⚠ Без выбранного инструмента спор будет проигран, так как ваши обязательства доказать "
                     "прогресс не смогут"
                     " быть выполнены. На видео обязательно должен быть четко слышен код.")

confirm_painting_msg = ("Для этой цели понадобится самостоятельно ежедневно рисовать на холсте/тетради или "
                        "планшете.\n\n"
                        "⚠ Принимаются видео только с процессом рисования. На видео обязательно должен быть четко "
                        "слышен код.")


def confirm_alcohol_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом и отрицательным алкотестом\n"
            "⌛ Отправлять в бот до 22:30\n\n")


second_msg = (f"Каждый день бот заранее присылает уведомление со специальным"
              f" кодом из четырех цифр, который тебе необходимо произнести на "
              f"видео, как в примере, и отправить в бот вовремя\.\n\n"
              f"👍Если всё ок, игра продолжится и вы сохраните свой депозит\n\n"
              f"👎Если правила игры нарушены, вы проиграете сначала 20% депозита, "
              f"а если это повторится — остальные 80%\.")


def confirm_smoking_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом и экспресс\-тестом на котинин\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_drugs_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом и экспресс\-тестом на необходимые ПАВ\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_gym_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом в зеркале спорт\-зала\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_weight_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео взвешивания с кодом\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_morning_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом в зеркале ванны\n")


def confirm_language_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом и конспектами\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_money_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Запись экрана из банка\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_food_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом и процессом\n"
            "⌛ Отправлять в бот до 22:30\n\n")


def confirm_programming_disput_msg(count_day):
    return (f"*Условия пари на {count_day}*\n"
            "🤳 Видео с кодом и процессом\n"
            "⌛ Отправлять в бот до 22:30\n\n")


months = {"January": "Января", "February": "Февраля", "March": "Марта", "April": "Апреля", "May": "Мая", "June": "Июня",
          "July": "Июля", "August": "Августа", "September": "Сентября", "October": "Октября",
          "November": "Ноября", "December": "Декабря"}


def get_timezone_msg(variant):
    # date_start = str(future_date.day) + " " + months[str(future_date.strftime('%B'))] + " " + str(future_date.year)

    choice_msg = ""
    tmp_keyboard = types.InlineKeyboardMarkup
    photo = InputFile
    count_day = "30 дней"
    if variant['is_blogger'] is True:
        count_day = "3 дня"

    promocode = variant['promocode']
    if promocode != '0':
        promocode = '1'

    if variant['action'] == 'alcohol':
        photo = InputFile("client/media/disputs_images/alcohol.jpg")
        choice_msg = f'{confirm_alcohol_disput_msg(count_day)}Право на ошибку:' \
                     f' {promocode}\n\n{second_msg} '
        tmp_keyboard = alcohol_deposit_keyboard

    elif variant['action'] == 'smoking':
        photo = InputFile("client/media/disputs_images/smoking.jpg")
        choice_msg = f'{confirm_smoking_disput_msg(count_day)}Право на ошибку:' \
                     f' {promocode}\n\n{second_msg} '
        tmp_keyboard = smoking_deposit_keyboard

    elif variant['action'] == 'drugs':
        photo = InputFile("client/media/disputs_images/drugs.jpg")
        choice_msg = f'{confirm_drugs_disput_msg(count_day)}Право на ошибку:' \
                     f' {promocode}\n\n{second_msg}'
        tmp_keyboard = drugs_deposit_keyboard

    elif variant['action'] == 'gym':
        photo = InputFile("client/media/disputs_images/gym.jpg")
        choice_msg = f'{confirm_gym_disput_msg(count_day)}Право на ошибку:' \
                     f' {promocode}\n\n{second_msg}'
        tmp_keyboard = gym_deposit_keyboard

    elif variant['action'] == 'weight':
        photo = InputFile("client/media/disputs_images/weight.jpg")
        choice_msg = f'{confirm_weight_disput_msg(count_day)}Право на ошибку:' \
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

        choice_msg = f'{confirm_morning_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
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
        choice_msg = f'{confirm_language_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = language_deposit_keyboard

    elif variant['action'] == 'money':
        if variant['additional_action'] == 'hundred':
            photo = InputFile("client/media/disputs_images/hundred.jpg")
        elif variant['additional_action'] == 'three_hundred':
            photo = InputFile("client/media/disputs_images/three_hundred.jpg")
        choice_msg = f'{confirm_money_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = money_deposit_keyboard

    elif variant['action'] == 'food':
        photo = InputFile("client/media/disputs_images/food.jpg")
        choice_msg = f'{confirm_food_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = food_deposit_keyboard

    elif variant['action'] == 'programming':
        photo = InputFile("client/media/disputs_images/programming.jpg")
        choice_msg = f'{confirm_programming_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = programming_deposit_keyboard

    elif variant['action'] == 'instruments':
        if variant['additional_action'] == 'piano':
            photo = InputFile("client/media/disputs_images/piano.jpg")
        elif variant['additional_action'] == 'guitar':
            photo = InputFile("client/media/disputs_images/guitar.jpg")
        choice_msg = f'{confirm_programming_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = instruments_deposit_keyboard

    elif variant['action'] == 'painting':
        photo = InputFile("client/media/disputs_images/painting.jpg")
        choice_msg = f'{confirm_programming_disput_msg(count_day)}Право на ошибку: {promocode}\n\n{second_msg}'
        tmp_keyboard = painting_deposit_keyboard

    return photo, choice_msg, tmp_keyboard
