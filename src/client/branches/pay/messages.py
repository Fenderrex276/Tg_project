from aiogram import types

deposit_msg = ("Твой депозит будет заморожен "
               "в Диспуте до момента победы в споре "
               "и будет доступен для мгновенного вывода"
               " в любое время или начала следующей игры")

other_sum_msg = ("Введи комфортную сумму в рублях (только цифра, без копеек)."
                 " Депозит не может быть меньше 15000 ₽ и не больше 150000 ₽")

application_for_payment_msg = ("*Ваша заявка #TG3042 создана*\n"
                               "Вам выделяется на оплату 30 минут с момента получения реквизитов.\n"
                               " Обработка заявок круглосуточная.\n\n"
                               "По истечению времени, заявка снимается с оплаты. "
                               "Вы можете открыть новый Диспут и создать новую заявку.\n\n"
                               "После оплаты ожидайте автоматического подтверждения платежа и сообщение о том, "
                               "что ваша заявка оплачена.\n\n"
                               "В случае, если через 15 минут вы не получили подтверждения, "
                               "свяжитесь с нами по кнопке «Проблема с оплатой».")


def starting_message_dispute(data, name):
    purpose = ""
    video_with_code = ""
    time_before = "22:30"
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
    n_d = '30 дней'
    if data['count_days'] == 3:
        n_d = '3 дня'

    return (f"👋 Привет, {name},"
            f" заверши свою подготовку к цели и начни путь героя.\n\n"
            "*Твоя цель:*\n"
            f"{purpose}\n"
            f"🧊 Депозит: {data['deposit']} ₽ \n\n"
            f"*Условия на {n_d}*\n"
            f"{video_with_code}\n"
            f"⏳ Отправлять в бот до {time_before}\n\n"
            f"До победы осталось {n_d}\n"
            f"Право на ошибку: {promo}")
