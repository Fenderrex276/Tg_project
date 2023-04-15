from aiogram.types import InputFile
from ..confirm_dispute.messages import test_alcohol_link, test_smoke_link, test_pav_link, test_pav_link2

algorithm_msg = ("Разбивая каждую цель на этапы, можно определить точки,"
                 " в которых будет возможно доказать свой путь и "
                 "отследить прогресс. Для этого мы "
                 "разработали уникальную систрему репортов.")

algorithm_msg2 = ("Каждый день бот заранее присылает уведомление со "
                  "специальным кодом из четырёх цифр, который "
                  "тебе необходимо произнести на видео, как в примере, "
                  "и отправить вовремя в бот.\n"
                  "👍 Если все ок, игра продолжится и ты сохранишь свой депозит\n\n"
                  "👎 Если правила спора нарушены, – "
                  "проиграешь сначала 20% депозита, а если это повторится — остальные 80%.\n\n"
                  "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру.")

send_video_alcohol_msg = ("⏰ Отправь до 00:00 кружочек с тестом на алкоголь"
                          " (даже если он пока положительный), как на примере, произнеси код 🔒 3 0 2 8")

send_video_smoking_msg = ("⏰ Отправь до 00:00 кружочек с тестом на никотин "
                          "(даже если он пока положительный), оторви полоску как на примере, произнеси код 🔒 3 0 2 8")

send_video_drugs_msg = ("⏰ Отправь до 00:00 кружочек с тестом на ПАВ "
                        "(даже если он пока положительный), оторви полоску, как на примере, произнеси код 🔒 3 0 2 8")

send_video_gym_msg = ("⏰ Отправь до 00:00 кружочек в зеркале в спорт-зале, "
                      "как на примере, произнеси код 🔒 3 0 2 8")

send_video_weight_msg = ("⏰ Отправь до 00:00 кружочек своего взвешивания,"
                         " как на примере, произнеси код 🔒 3 0 2 8")

send_video_morning_msg = "⏰ Отправь до 00:00 кружочек в зеркале, как на примере, произнеси код 🔒 3 0 2 8"

send_video_language_msg = ("⏰ Отправь до 00:00 кружочек с конспектами своего занятия, "
                           "как на примере, произнеси код 🔒 3 0 2 8")

send_video_bank_msg = ("⏰ Отправь до 00:00 видео-запись экрана со своего нового специального депозитного счета с"
                       " нулевым балансом, как на примере, на видео должен быть код 🔒 3 0 2 8")

send_video_food_msg = ("⏰ Отправь до 00:00 кружочек процесса приготовления здоровой еды,"
                       " как на примере, произнеси код 🔒 3 0 2 8")

send_video_programming_msg = ("⏰ Отправь до 00:00 кружочек процесса программирования,"
                              " как на примере, произнеси код 🔒 3 0 2 8")

send_video_instrument_msg = ("⏰ Отправь до 00:00 кружочек процесса занятий на муз."
                             " инструменте, как на примере, произнеси код 🔒 3 0 2 8")

send_video_painting_msg = "⏰ Отправь до 00:00 кружочек процесса рисования, как на примере, произнеси код 🔒 3 0 2 8"

success_msg = "Отлично 🔥 У тебя всё получилось"

code_msg = "Твой новый код придёт сюда завтра."

pin_chat_msg = "Для того, чтобы сохранять фокус на цели и не терять важные уведомления в списке чатов, закрепи" \
               " 📌 Диспут наверху и нажми «Готово». Никакого спама. Только важное."

pav_msg = (f"Для этой цели понадобится самостоятельно приобрести {test_pav_link}\.\n\n"
           f"{test_pav_link2}\n\n"
           "⚠️ Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать прогресс"
           " не смогут быть выполнены\.\n\n"
           "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру\."
           " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем "
           "за 6 дней, иначе на 7 день спор будет проигран\.")

niko_msg = ("Для этой цели понадобится самостоятельно приобрести экспресс\-тесты \(30 шт на 30 дней\) на котинин\.\n\n"
            f"{test_smoke_link}\n\n"
            "⚠️ Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать прогресс"
            " не смогут быть выполнены\.\n\n"
            "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру\."
            " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6"
            " дней, иначе на 7 день спор будет проигран\.")

alco_msg = ("Для этой цели понадобится самостоятельно приобрести экспресс\-тесты \(30 шт на 30 дней\) на алкоголь\.\n\n"
            f"{test_alcohol_link}\n\n"
            "⚠️ Без самостоятельной покупки тестов спор будет проигран, так как ваши обязательства доказать прогресс "
            "не смогут быть выполнены\.\n\n"
            "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит "
            "и игру\. Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не "
            "более чем за 6 дней, иначе на 7 день спор будет проигран\.")

gym_msg = ("Для этой цели понадобится самостоятельно приобрести абонемент в фитнес-клуб на 1 месяц.\n\n"
           "⚠️ Без абонемента спор будет проигран, так как ваши обязательства доказать прогресс не смогут быть "
           "выполнены. В случаях, если ваш зал не будет работать в выходные и"
           " праздники - ваша задача попасть в другой зал или на спорт-площадку.\n\n"
           "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру."
           " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более "
           "чем за 6 дней, иначе на 7 день спор будет проигран.")

wei_msg = ("Для этой цели понадобится ежедневно взвешиваться на исправных электронных весах.\n\n"
           "⚠️ Не важно, теряешь ли ты вес каждый день или нет. Важно к концу 30 дня быть легче первоначального веса"
           " на 5 кг, даже если получится достичь результата раньше. Можно снимать себя без лица, главное,"
           " чтобы на видео был четко слышен уникальный код и вы отправляли его вовремя.\n\n"
           "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру."
           " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем"
           " за 6 дней, иначе на 7 день спор будет проигран.")

morn_msg = ("Для этой цели понадобится ежедневно просыпаться рано утром и делать короткое видео в зеркале ванны.\n\n"
            "⚠️ Можно снимать себя без лица, главное, чтобы на видео был четко слышен уникальный код и вы отправляли"
            " его вовремя.\n\n"
            "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру."
            " Вы можете "
            "бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6 дней, иначе на 7"
            " день спор будет проигран.")

lang_msg = (
    "Для этой цели понадобится ежедневно уделять время изучению языка. Учить новые слова и делать конспекты упражнений.\n\n"
    "⚠️ Постарайтесь делать записи новых слов или правил в отдельную тетрадь. Без письменных свидетельств учебы "
    "спор будет проигран, так как ваши обязательства доказать прогресс не смогут быть выполнены, если вы "
    "занимаетесь исключительно на сайте или в приложениях. На видео обязательно должен быть слышен код.\n\n"
    "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру."
    " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более "
    "чем за 6 дней, иначе на 7 день спор будет проигран.")

money_msg = (
    "Для этой цели понадобится создать накопительный счёт в приложении любого банка, чтобы ежедневно делать "
    "видео-запись экрана истории пополнений, даже если пополнений в этот день не было.\n\n"
    "⚠️ Важно к концу 30 дня иметь на счету загаданную сумму, даже если получится достичь результата раньше."
    "На каждой записи экрана обязательно должен быть четко виден ваш код, который приходит каждое утро.\n\n"
    "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру."
    " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6 дней,"
    " иначе на 7 день спор будет проигран.")

eat_msg = ("Для этой цели понадобится самостоятельно ежедневно готовить здоровую еду.\n\n"
           "⚠️ Принимаются видео только с процессом приготовления еды, а не с готовым блюдом."
           " На видео обязательно должен быть четко слышен код.\n\n"
           "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру. "
           "Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более "
           "чем за 6 дней, иначе на 7 день спор будет проигран.")

prog_msg = ("Для этой цели понадобится самостоятельно ежедневно программировать.\n\n"
            "⚠️ Принимаются видео только с процессом программирования."
            "На видео обязательно должен быть четко слышен код.\n\n"
            "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру."
            " Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более "
            "чем за 6 дней, иначе на 7 день спор будет проигран.")

mus_msg = ("Для этой цели понадобится самостоятельно ежедневно играть на музыкальном инструменте.\n\n"
           "⚠️ Без выбранного инструмента спор будет проигран, так как ваши обязательства доказать прогресс "
           "не смогут быть выполнены. "
           "На видео обязательно должен быть четко слышен код.\n\n"
           "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит"
           " и игру. Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не "
           "более чем за 6 дней, иначе на 7 день спор будет проигран.")

paint_msg = ("Для этой цели понадобится самостоятельно ежедневно рисовать на холсте/тетради или планшете.\n\n"
             "⚠️ Принимаются видео только с процессом рисования. На видео обязательно должен быть четко слышен код.\n\n"
             "⚠️ Ошибки на этапе подготовки — нормально, и это никак не влияет на депозит и игру. "
             "Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не "
             "более чем за 6 дней, иначе на 7 день спор будет проигран.")


def message_to_training(data):
    video = InputFile
    tmp_msg = ""
    if data['action'] == 'alcohol':
        tmp_msg = send_video_alcohol_msg
        video = InputFile("client/media/videos/alcohol.mp4")
    elif data['action'] == 'drugs':
        tmp_msg = send_video_drugs_msg
        video = InputFile("client/media/videos/drugs.mp4")
    elif data['action'] == 'smoking':
        tmp_msg = send_video_smoking_msg
        video = InputFile("client/media/videos/smoke.mp4")
    elif data['action'] == 'gym':
        tmp_msg = send_video_gym_msg
        video = InputFile("client/media/videos/gym.mp4")
    elif data['action'] == 'weight':
        tmp_msg = send_video_weight_msg
        video = InputFile("client/media/videos/weight.mp4")
    elif data['action'] == 'morning':
        tmp_msg = send_video_morning_msg
        video = InputFile("client/media/videos/morning.mp4")
    elif data['action'] == 'language':
        tmp_msg = send_video_language_msg
        video = InputFile("client/media/videos/language.mp4")
    elif data['action'] == 'money':
        tmp_msg = send_video_bank_msg
        video = InputFile("client/media/videos/bank.mp4")
    elif data['action'] == 'food':
        tmp_msg = send_video_food_msg
        video = InputFile("client/media/videos/food.mp4")
    elif data['action'] == 'programming':
        tmp_msg = send_video_programming_msg
        video = InputFile("client/media/videos/programming.mp4")
    elif data['action'] == 'instruments':
        tmp_msg = send_video_instrument_msg
        if data['additional_action'] == 'piano':
            video = InputFile("client/media/videos/piano.mp4")
        elif data['additional_action'] == 'guitar':
            video = InputFile("client/media/videos/guitar.mp4")
    elif data['action'] == 'painting':
        tmp_msg = send_video_painting_msg
        video = InputFile("client/media/videos/painting.mp4")

    return tmp_msg, video


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