from aiogram.types import InputFile

from client.branches.confirm_dispute.messages import test_pav_link, test_pav_link2, test_smoke_link, test_alcohol_link


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
    start_current_disput_msg = (f"🚩 *До победы осталось {count_days} {day}*\n\n"
                                f"Условия на {n_days}\n"
                                f"{video_with_code}\n"
                                f"⏳ Отправлять в бот до {time_before}\n\n"

                                f"💰 Депозит: {deposit} ₽ \n\n")

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


pav_msg = (f"Для этой цели понадобится самостоятельно приобрести {test_pav_link}\.\n\n"
           f"{test_pav_link2}\n\n"
           "⚠️ Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать прогресс"
           " не смогут быть выполнены\.")

niko_msg = ("Для этой цели понадобится самостоятельно приобрести экспресс\-тесты \(30 шт на 30 дней\) на котинин\.\n\n"
            f"{test_smoke_link}\n\n"
            "⚠️ Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать прогресс"
            " не смогут быть выполнены\.")

alco_msg = ("Для этой цели понадобится самостоятельно приобрести экспресс\-тесты \(30 шт на 30 дней\) на алкоголь\.\n\n"
            f"{test_alcohol_link}\n\n"
            "⚠️ Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать прогресс "
            "не смогут быть выполнены\.")

gym_msg = ("Для этой цели понадобится самостоятельно приобрести абонемент в фитнес-клуб на 1 месяц.\n\n"
           "⚠️ Без абонемента спор будет проигран, так как ваши обязательства доказать прогресс не смогут быть "
           "выполнены. В случаях, если ваш зал не будет работать в выходные и"
           " праздники - ваша задача попасть в другой зал или на спорт-площадку.")

wei_msg = ("Для этой цели понадобится ежедневно взвешиваться на исправных электронных весах.\n\n"
           "⚠️ Не важно, теряешь ли ты вес каждый день или нет. Важно к концу 30 дня быть легче первоначального веса"
           " на 5 кг, даже если получится достичь результата раньше. Можно снимать себя без лица, главное,"
           " чтобы на видео был четко слышен уникальный код и вы отправляли его вовремя.")

morn_msg = ("Для этой цели понадобится ежедневно просыпаться рано утром и делать короткое видео в зеркале ванны.\n\n"
            "⚠️ Можно снимать себя без лица, главное, чтобы на видео был четко слышен уникальный код и вы отправляли"
            " его вовремя.")

lang_msg = (
    "Для этой цели понадобится ежедневно уделять время изучению языка. Учить новые слова и делать конспекты упражнений.\n\n"
    "⚠️ Постарайтесь делать записи новых слов или правил в отдельную тетрадь. Без письменных свидетельств учебы "
    "спор будет проигран, так как ваши обязательства доказать прогресс не смогут быть выполнены, если вы "
    "занимаетесь исключительно на сайте или в приложениях. На видео обязательно должен быть слышен код.")

money_msg = (
    "Для этой цели понадобится создать накопительный счёт в приложении любого банка, чтобы ежедневно делать "
    "видео-запись экрана истории пополнений, даже если пополнений в этот день не было.\n\n"
    "⚠️ Важно к концу 30 дня иметь на счету загаданную сумму, даже если получится достичь результата раньше."
    "На каждой записи экрана обязательно должен быть четко виден ваш код, который приходит каждое утро.")

eat_msg = ("Для этой цели понадобится самостоятельно ежедневно готовить здоровую еду.\n\n"
           "⚠️ Принимаются видео только с процессом приготовления еды, а не с готовым блюдом."
           " На видео обязательно должен быть четко слышен код.")

prog_msg = ("Для этой цели понадобится самостоятельно ежедневно программировать.\n\n"
            "⚠️ Принимаются видео только с процессом программирования."
            "На видео обязательно должен быть четко слышен код.")

mus_msg = ("Для этой цели понадобится самостоятельно ежедневно играть на музыкальном инструменте.\n\n"
           "⚠️ Без выбранного инструмента спор будет проигран, так как ваши обязательства доказать прогресс "
           "не смогут быть выполнены. "
           "На видео обязательно должен быть четко слышен код.")

paint_msg = ("Для этой цели понадобится самостоятельно ежедневно рисовать на холсте/тетради или планшете.\n\n"
             "⚠️ Принимаются видео только с процессом рисования. На видео обязательно должен быть четко слышен код.")


def message_to_prepare(data):
    tmp_msg = ""
    if data['action'] == 'alcohol':
        tmp_msg = alco_msg
    elif data['action'] == 'drugs':
        tmp_msg = pav_msg
    elif data['action'] == 'smoking':
        tmp_msg = niko_msg
    elif data['action'] == 'gym':
        tmp_msg = gym_msg
    elif data['action'] == 'weight':
        tmp_msg = wei_msg
    elif data['action'] == 'morning':
        tmp_msg = morn_msg
    elif data['action'] == 'language':
        tmp_msg = lang_msg
    elif data['action'] == 'money':
        tmp_msg = money_msg
    elif data['action'] == 'food':
        tmp_msg = eat_msg
    elif data['action'] == 'programming':
        tmp_msg = prog_msg
    elif data['action'] == 'instruments':
        tmp_msg = mus_msg
    elif data['action'] == 'painting':
        tmp_msg = paint_msg

    return tmp_msg


def rules_msg(start_time_dispute, promocode, data):
    part_msg = message_to_prepare(data)
    if data['action'] in ['alcohol', 'smoking', 'drugs']:
        msg = ("😇 Правила диспута\n\n"
               f"Мы принимаем твой репорт в этом диспуте {start_time_dispute}\.\n\n"
               "Каждый день бот присылает уведомление со специальным кодом из четырёх цифр, "
               "который тебе необходимо произнести на видео, как в примере, и отправить в бот вовремя\.\n\n"
               f"{part_msg}\n\n"
               "👍 Если все ок, игра продолжится и"
               "вы сохраните свой депозит\n\n"
               "👎 Если правила спора нарушены, вы проиграете сначала "
               "20\% депозита, а если это повторится — остальные 80\%\.\n\n"
               f"Право на ошибку: {promocode}")
    else:
        msg = ("😇 Правила диспута\n\n"
               f"Мы принимаем твой репорт в этом диспуте {start_time_dispute}.\n\n"
               "Каждый день бот присылает уведомление со специальным кодом из четырёх цифр, "
               "который тебе необходимо произнести на видео, как в примере, и отправить в бот вовремя.\n\n"
               f"{part_msg}\n\n"
               "👍 Если все ок, игра продолжится и"
               "вы сохраните свой депозит\n\n"
               "👎 Если правила спора нарушены, вы проиграете сначала "
               "20% депозита, а если это повторится — остальные 80%.\n\n"
               f"Право на ошибку: {promocode}")
    print(msg)
    return msg
