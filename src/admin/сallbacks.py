from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode


def current_dispute(dispute, additional_dispute):
    cur_msg = ""
    if dispute == "alcohol":
        cur_msg = "Цель: брошу пить алкоголь\nАлкотест"
    elif dispute == "drugs":
        cur_msg = "Цель: брошу употреблять ПАВ\nЭкспресс-тест на ПАВ"
    elif dispute == "smoking":
        cur_msg = "Цель: брошу курить никотин\nЭкспресс-тест"
    elif dispute == "gym":
        cur_msg = "Цель: начну ходить в спорт-зал"
    elif dispute == "weight":
        cur_msg = "Цель: похудею на 5 кг"
    elif dispute == "morning":
        if additional_dispute == "five_am":
            cur_msg = "Цель: Буду вставать в 5 утра"
        elif additional_dispute == "six_am":
            cur_msg = "Цель: Буду вставать в 6 утра"
        elif additional_dispute == "seven_am":
            cur_msg = "Цель: Буду вставать в 7 утра"
        elif additional_dispute == "eight_am":
            cur_msg = "Цель: Буду вставать в 8 утра"
    elif dispute == "language":
        if additional_dispute == "english":
            cur_msg = "Цель: Буду учить английский язык"
        elif additional_dispute == 'chinese':
            cur_msg = "Цель: Буду учить китайский язык"
        elif additional_dispute == 'spanish':
            cur_msg = "Цель: Буду учить испанский язык"
        elif additional_dispute == 'arabian':
            cur_msg = "Цель: Буду учить арабский язык"
        elif additional_dispute == 'italian':
            cur_msg = "Цель: Буду учить итальянский язык"
        elif additional_dispute == 'french':
            cur_msg = "Цель: Буду учить французский язык"
    elif dispute == "money":
        if additional_dispute == "hundred":
            cur_msg = "Цель: Накоплю 100 000 ₽"
        elif additional_dispute == "three_hundred":
            cur_msg = "Цель: Накоплю 300 000 ₽"
    elif dispute == "food":
        cur_msg = "Научусь готовить здоровую еду"
    elif dispute == "programming":
        cur_msg = "Научусь программировать"
    elif dispute == "instruments":
        if additional_dispute == "piano":
            cur_msg = "Научусь играть на фортепиано"
        elif additional_dispute == "guitar":
            cur_msg = "Научусь играть на гитаре"
    elif dispute == "painting":
        cur_msg = "Научусь рисовать"

    return cur_msg
