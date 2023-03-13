from aiogram.types import InputFile


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
