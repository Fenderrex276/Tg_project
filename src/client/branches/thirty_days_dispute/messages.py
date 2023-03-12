from aiogram.types import InputFile


def video_text(data: dict, count_days: int, deposit: int):
    purpose = ""
    video_with_code = ""
    time_before = "22:30"

    if data['action'] == 'alcohol':
        purpose = "client/media/disputs_images/alcohol.jpg"
        video_with_code = "🤳 Видео с кодом и отрицательным алкотестом"

    elif data['action'] == 'smoking':
        purpose = "client/media/disputs_images/smoking.jpg"
        video_with_code = "🤳 Видео с кодом и экспресс-тестом"
    elif data['action'] == 'drugs':
        purpose = "client/media/disputs_images/drugs.jpg"
        video_with_code = "🤳 Видео с кодом и экспресс-тестом на ПАВ"
    elif data['action'] == "gym":
        purpose = "client/media/disputs_images/gym.jpg"
        video_with_code = "🤳 Видео с кодом в зеркале спорт-зала"
    elif data['action'] == "weight":
        purpose = "client/media/disputs_images/weight.jpg"
        video_with_code = "🤳 Видео взвешивания с кодом"
    elif data['action'] == "morning":
        if data['additional_action'] == 'five_am':
            time_before = "5:30"
            purpose = "client/media/disputs_images/five_am.jpg"
        elif data['additional_action'] == 'six_am':
            time_before = "6:30"
            purpose = "client/media/disputs_images/six_am.jpg"
        elif data['additional_action'] == 'seven_am':
            time_before = "7:30"
            purpose = "client/media/disputs_images/seven_am.jpg"
        elif data['additional_action'] == 'eight_am':
            time_before = "8:30"
            purpose = "client/media/disputs_images/eight_am.jpg"
        video_with_code = "🤳 Видео с кодом в зеркале ванны"
    elif data['action'] == "language":
        if data['additional_action'] == 'english':
            purpose = "client/media/disputs_images/english.jpg"
        elif data['additional_action'] == 'chinese':
            purpose = "client/media/disputs_images/chinese.jpg"
        elif data['additional_action'] == 'spanish':
            purpose = "client/media/disputs_images/spanish.jpg"
        elif data['additional_action'] == 'arabian':
            purpose = "client/media/disputs_images/arabian.jpg"
        elif data['additional_action'] == 'italian':
            purpose = "client/media/disputs_images/italian.jpg"
        elif data['additional_action'] == 'french':
            purpose = "client/media/disputs_images/french.jpg"
        video_with_code = "🤳 Видео с кодом и конспектами"
    elif data['action'] == 'money':

        if data['additional_action'] == 'hundred':
            purpose = "client/media/disputs_images/hundred.jpg"
        elif data['additional_action'] == 'three_hundred':
            purpose = "client/media/disputs_images/three_hundred.jpg"
        video_with_code = "🤳 Запись экрана из банка с кодом"
    elif data['action'] == 'food':
        purpose = "client/media/disputs_images/food.jpg"
        video_with_code = "🤳 Видео с кодом и процессом"
    elif data['action'] == 'programming':
        purpose = "client/media/disputs_images/programming.jpg"
        video_with_code = "🤳 Видео с кодом и процессом"
    elif data['action'] == 'instruments':
        if data['additional_action'] == 'piano':
            purpose = "client/media/disputs_images/piano.jpg"
        elif data['additional_action'] == 'guitar':
            purpose = "client/media/disputs_images/guitar.jpg"
        video_with_code = "🤳 Видео с кодом и процессом"
    elif data['action'] == 'painting':
        purpose = "client/media/disputs_images/painting.jpg"
        video_with_code = "🤳 Видео с кодом и процессом"
    day = "дней"
    if count_days == 3:
        day = "дня"

    n_days = "30 дней"
    if data['is_blogger'] is True:
        n_days = "3 дня"
    start_current_disput_msg = (f"*До победы осталось {count_days} {day}*\n\n"
                                f"Условия на {n_days}\n"
                                f"{video_with_code}\n"
                                f"⏳ Отправлять в бот до {time_before}\n\n"

                                f"🧊 Депозит: {deposit} ₽ \n\n")

    return [purpose, start_current_disput_msg]


def get_time_to_send_dispute(data):
    time_t = 22

    if data['action'] == 'morning':
        if data['additional_action'] == 'five_am':
            time_t = 5
        elif data['additional_action'] == 'six_am':
            time_t = 6
        elif data['additional_action'] == 'seven_am':
            time_t = 7
        elif data['additional_action'] == 'eight_am':
            time_t = 8
    return (f"⌛️ Время для отправки репорта истекло. По правилам Диспута, "
            f"мы ждём твой репорт каждый день до {time_t}:30 утра.")


def get_message_video(data, new_code):
    tmp_msg = ""
    video = ""
    if data['action'] == 'alcohol':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек с тестом на алкоголь"
                   f" как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/alcohol.mp4"
    elif data['action'] == 'drugs':
        tmp_msg = ("⏰ Отправь до 00:00 кружочек с тестом на ПАВ "
                   "(даже если он пока положительный), оторви полоску,"
                   f" как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/drugs.mp4"
    elif data['action'] == 'smoking':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек с тестом на никотин "
                   "(даже если он пока положительный), оторви полоску как на "
                   f"примере, произнеси код 🔒 {new_code}")

        video = "client/media/videos/smoke.mp4"
    elif data['action'] == 'gym':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек в зеркале в спорт-зале, "
                   f"как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/gym.mp4"
    elif data['action'] == 'weight':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек своего взвешивания,"
                   f" как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/weight.mp4"
    elif data['action'] == 'morning':
        if data['additional_action'] == 'five_am':
            tmp_msg = f"⏰ Отправь до 5:30 кружочек в зеркале, как на примере, произнеси код 🔒 {new_code}"
        elif data['additional_action'] == 'six_am':
            tmp_msg = f"⏰ Отправь до 6:30 кружочек в зеркале, как на примере, произнеси код 🔒 {new_code}"
        elif data['additional_action'] == 'seven_am':
            tmp_msg = f"⏰ Отправь до 7:30 кружочек в зеркале, как на примере, произнеси код 🔒 {new_code}"
        elif data['additional_action'] == 'eight_am':
            tmp_msg = f"⏰ Отправь до 8:30 кружочек в зеркале, как на примере, произнеси код 🔒 {new_code}"
        video = "client/media/videos/morning.mp4"
    elif data['action'] == 'language':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек с конспектами своего занятия, "
                   f"как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/language.mp4"
    elif data['action'] == 'money':
        tmp_msg = ("⏰ Отправь до 22:30 видео-запись экрана со своего специального депозитного счета,"
                   f" как на примере, на видео должен быть код 🔒 {new_code}")
        video = "client/media/videos/bank.mp4"
    elif data['action'] == 'food':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек процесса приготовления здоровой еды,"
                   f" как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/food.mp4"
    elif data['action'] == 'programming':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек процесса программирования,"
                   f" как на примере, произнеси код 🔒 {new_code}")
        video = "client/media/videos/programming.mp4"
    elif data['action'] == 'instruments':
        tmp_msg = ("⏰ Отправь до 22:30 кружочек процесса занятий на муз."
                   f" инструменте, как на примере, произнеси код 🔒 {new_code}")
        if data['additional_action'] == 'piano':
            video = InputFile("client/media/videos/piano.mp4")
        elif data['additional_action'] == 'guitar':
            video = InputFile("client/media/videos/guitar.mp4")
    elif data['action'] == 'painting':
        tmp_msg = f"⏰ Отправь до 22:30 кружочек процесса рисования, как на примере, произнеси код 🔒 {new_code}"
        video = "client/media/videos/painting.mp4"

    return [tmp_msg, video]
