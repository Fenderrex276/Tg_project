import random
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from .diary import questions
from .keyboards import *
from .states import StatesDispute
from db.models import RoundVideo
from ..confirm_dispute.keyboards import choose_time_zone_keyboard



async def begin_dispute(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.none.set()

    data = await state.get_data()
    recieve_message = video_text(data)
    await call.message.answer_photo(photo=InputFile(recieve_message[0]), caption=recieve_message[1],
                                    reply_markup=menu_keyboard,
                                    parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def video_text(data: dict):
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

    start_current_disput_msg = ("*До победы осталось 30 дней*\n\n"
                                "Условия на 30 дней\n"
                                f"{video_with_code}\n"
                                f"⏳ Отправлять в бот до {time_before}\n\n"

                                f"🧊 Депозит: {data['deposit']} ₽ \n\n")

    return [purpose, start_current_disput_msg]


async def reports(call: types.CallbackQuery):
    main_photo = InputFile("client/media/days_of_dispute/zero_day.jpg")
    await call.message.answer_photo(main_photo, reply_markup=report_keyboard)
    await call.answer()


async def choose_name_button(call: types.CallbackQuery, state: FSMContext):
    user = await state.get_data()
    msg = (f"💎 В твоём профиле Телеграмм указано имя "
           f"{user['name']}. Впиши сюда любое другое, "
           "если хочешь изменить своё имя в Диспуте")

    await call.message.edit_text(text=msg, reply_markup=change_name_keyboard)
    await call.answer()


async def change_name(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.change_name.set()
    msg = "💬 Введи своё новое имя:"

    await call.message.edit_text(text=msg)
    await call.answer()


async def check_report(call: types.CallbackQuery, state: FSMContext):

    try:
        user_video = await RoundVideo.objects.aget(user_tg_id=call.from_user.id,
                                                   chat_tg_id=call.message.chat.id,
                                                   type_video=RoundVideo.TypeVideo.dispute
                                                   )
        data = await state.get_data()
        # user_video = await RoundVideo.objects.aget(id_video=data['id_video_code'])
        if user_video.status == "" and user_video.tg_id != "":
            tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."
            await call.message.answer(text=tmp_msg)
            await state.update_data(id_video_code="")
        else:
            new_code = " ".join(list(user_video.code_in_video))
            temp_array = get_message_video(data, new_code)
            await call.message.answer(text=temp_array[0])
            await state.update_data(new_code=user_video.code_in_video, id_video_code=user_video.id_video)
            if data['action'] == 'money':
                await StatesDispute.video.set()
                await call.message.answer_video(video=InputFile(temp_array[1]))
            else:
                await StatesDispute.video_note.set()
                await call.message.answer_video_note(video_note=InputFile(temp_array[1]))
    except:
        await call.message.answer(text='Твой новый код придёт в бот автоматически.')
    await call.answer()


async def recieved_video(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await StatesDispute.none.set()
    await RoundVideo.objects.filter(chat_tg_id=call.message.chat.id,
                                    type_video=RoundVideo.TypeVideo.dispute,
                                    id_video=data['id_video_code']).aupdate(tg_id=data['video_id'])
    tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."
    await call.message.answer(text=tmp_msg)
    await call.answer()


async def send_new_report_from_admin(call: types.CallbackQuery, state: FSMContext):
    # print(call.from_user.id, call.message.chat.id)
    new_video = await RoundVideo.objects.aget(user_tg_id=call.from_user.id,
                                              chat_tg_id=call.message.chat.id,
                                              type_video=RoundVideo.TypeVideo.dispute
                                              )
    print(new_video.id_video)
    data = await state.get_data()

    await state.update_data(new_code=new_video.code_in_video, id_video_code=new_video.id_video)

    new_code = " ".join(list(new_video.code_in_video))
    temp_array = get_message_video(data, new_code)

    await call.message.answer(text=temp_array[0])

    if data['action'] == 'money':
        await StatesDispute.video.set()
        await call.message.answer_video(video=InputFile(temp_array[1]))
    else:
        await StatesDispute.video_note.set()
        await call.message.answer_video_note(video_note=InputFile(temp_array[1]))
    await call.answer()


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

        video = "client/media/videos/piano.mp4"
    elif data['action'] == 'painting':
        tmp_msg = f"⏰ Отправь до 22:30 кружочек процесса рисования, как на примере, произнеси код 🔒 {new_code}"
        video = "client/media/videos/painting.mp4"

    return [tmp_msg, video]


async def diary_button(call: types.CallbackQuery, state: FSMContext):
    msg = ("📝 Исповедь — это честный диалог "
           "с самим собой, со своим внутренним «Я» в интерактивной форме.\n\n"
           "Исповедь подразумевает признание"
           "в чём-либо. Как известно, признание проблемы — первый шаг на пути "
           "к её решению.\n\n"
           "Бот будет отправлять вопросы, ты можешь дать свой ответ или пропустить вопрос. Твои ответы никуда не "
           "отправляются и "
           "остаются здесь, наедине с тобой.\n\n"
           "Перечитай и проанализируй их, посмотри на ситуации и себя со стороны и продолжай свой путь")
    await state.update_data(number_question=random.randint(0, 29))
    await call.message.answer(text=msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='🎲 Рандомно', callback_data='random_questions')))
    await call.answer()


async def random_question(call: types.CallbackQuery, state: FSMContext):
    number = await state.get_data()
    ind = number['number_question']
    second_ind = random.randint(0, 29)
    if second_ind == ind:
        second_ind = random.randint(0, 29)
    await state.update_data(number_question=second_ind)
    await call.message.answer(text=questions[second_ind], reply_markup=admit_or_pass_keyboard)
    await call.answer()


async def admit_answer(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.diary.set()
    msg = "💬 Пиши всё, что придёт в голову:"
    await call.message.answer(text=msg)
    await call.answer()


async def next_question(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    number = await state.get_data()
    ind = number['number_question']
    second_ind = random.randint(0, 29)
    if second_ind == ind:
        second_ind = random.randint(0, 29)
    await state.update_data(number_question=second_ind)
    await call.message.answer(text=questions[second_ind], reply_markup=admit_or_pass_keyboard)
    await call.answer()


async def dispute_rules(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    start_time_dispute = ""
    array = ['alcohol', 'drugs', 'smoking', 'gym', 'weight', 'language', 'programming', 'paint', 'food',
             'instruments']

    if data['action'] in array:
        start_time_dispute = "6:00 до 22:30 вечера."
    else:
        if data['additional_action'] == 'five_am':
            start_time_dispute = "5:00–5:30 утра."
        elif data['additional_action'] == 'six_am':
            start_time_dispute = "6:00–6:30 утра."
        elif data['additional_action'] == 'seven_am':
            start_time_dispute = "7:00–7:30 утра."
        elif data['additional_action'] == 'eight_am':
            start_time_dispute = "8:00–8:30 утра."

    tmp_msg = ("😇 Правила диспута\n\n"
               f"Мы принимаем твой репорт в этом диспуте в период с {start_time_dispute}\n\n"
               "Каждый день бот присылает уведомление со специальным кодом из четырёх цифр, "
               "который тебе необходимо произнести на видео, как в примере, и отправить в бот вовремя.\n\n"
               "👍 Если все ок, игра продолжится и"
               "вы сохраните свой депозит"
               "👎 Если правила спора нарушены, вы проиграете сначала "
               "20% депозита, а если это повторится — остальные 80%.\n\n"
               f"Право на ошибку: {data['promocode']}")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='👍 Спасибо', callback_data='Thanks1')))
    await call.answer()


async def return_reports(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_caption(caption="", reply_markup=report_keyboard)
    await call.answer()


async def awards(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = ("👑 Бонусы — 0 ₽\n\n"
               "Выбери задание и зарабатывай дополнительные 💰 в свой депозит")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=awards_keyboard)
    await call.answer()


async def promo_code_awards(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = ("🎟 Рассказывай друзьям и подписчикам о том, как проходишь свой путь и дари 🎁 промо-код "
               "на право одной ошибки без потери депозита в Диспуте.\n\n"
               "Получай дополнительные 1 000 ₽ на счёт своего депозита за каждого, кто примет вызов"
               " и сразится с собой.\n\n"
               "Делись своим промо-кодом в любых социальных сетях с указанием "
               "ссылки на бот – t.me/Dlspute_bot")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='🎟 Мой код', callback_data='user_promocode'),
        types.InlineKeyboardButton(text='Назад', callback_data='back_awards')))
    await call.answer()


async def my_promocode(call: types.CallbackQuery, state: FSMContext):
    sobchak = "SOBCHAK"
    await call.message.answer(text=sobchak)
    await call.message.answer(text='Зажми промо-код, чтобы скопировать')
    await call.answer()


async def dispute_awards(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = ("⭐️ Отправь свой лучший кружочек "
               "на ежемесячный конкурс DisputeAward.\n\n"

               "На твой пример смогут ровняться "
               "тысячи игроков, а ты заработаешь"
               "+5 000 ₽ к своему депозиту.\n\n"

               "Можно отправить только 1 видео / мес.")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='👀 Выбрать', callback_data='choose_video_to_dispute_award')))
    await call.answer()


async def deposit_button(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tmp_msg = (f"*💰 Депозит: {data['deposit']} ₽*\n"
               f"{data['deposit']} ₽ \+ 0 ₽ бонусов\n\n"
               "Твой депозит и бонусы заморожены в Диспуте до момента победы в споре и будут доступны для вывода "
               "или для начала следующей игры\n\n"
               "⚠️️ Бонусы отдельно без депозита не подлежат выводу\\.")

    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Вывод 💰', callback_data='withdrawal_deposit'),
        types.InlineKeyboardButton(text='Личные 🎯️ цели', callback_data='personal_goals')),
                              parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()


async def withdraw_deposit(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = ("🚩*До победы осталось 30 дней\.*\n\n"

               "Пройди свой Путь Героя и вывод твоего депозита на банковскую "
               "карту или в BTC станет доступен в этом окне")

    await call.message.answer(text=tmp_msg, parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()


async def change_timezone(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tmp_msg = f"🌍 Установлен часовой пояс {data['timezone']} UTC"
    geo_position_msg = (
        "🌍 Укажи разницу во времени относительно UTC (Москва +3, Красноярск +7 и тд) или отправь в бот "
        "геопозицию (возьмем только часовой пояс)")

    await call.message.answer(text=tmp_msg)
    await call.message.answer(text=geo_position_msg, reply_markup=choose_time_zone_keyboard)
    await call.answer()


async def return_account(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.account.set()
    user = await state.get_data()
    msg = (f"👋 *Привет, {user['name']}* \n\n"
           "Здесь ты можешь изменить своё имя, вывести выигранный депозит, "
           "изменить свой часовой пояс или написать свой вопрос в тех. "
           "поддержку через форму обратной связи.")

    await call.message.edit_text(text=msg, reply_markup=account_keyboard, parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def new_time_zone(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(timezone=call.data)
    tmp_msg = f"Установлен часовой пояс {call.data} UTC"
    await call.message.answer(text=tmp_msg)
    await call.answer()


async def support_button(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = ("🆘 *Поддержка*\n\n"

               "Расскажи о технической ошибке, если столкнёшься с этим в процессе, и наши арбитры оперативно придут "
               "на помощь.\n\n"

               "Будем очень благодарны твоему опыту взаимодействия с ботом и в сложных случаях всегда будем на твоей "
               "стороне 🤝")

    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Сообщить о проблеме', callback_data='send_new_support')),
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def new_support_question(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.new_question.set()

    await call.message.answer(text='💬 Введи сообщение:')
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(begin_dispute, text='go_dispute', state="*")
    dp.register_callback_query_handler(reports, text='report', state=StatesDispute.none)
    dp.register_callback_query_handler(choose_name_button, text='change_name', state=StatesDispute.account)
    dp.register_callback_query_handler(change_name, text='change_name_access', state=StatesDispute.account)
    dp.register_callback_query_handler(check_report, text="send_new_report", state="*")
    dp.register_callback_query_handler(send_new_report_from_admin, text="send_dispute_report", state="*")
    dp.register_callback_query_handler(diary_button, text='diary', state=StatesDispute.none)
    dp.register_callback_query_handler(random_question, text='random_questions', state=StatesDispute.none)
    dp.register_callback_query_handler(admit_answer, text='admit', state=StatesDispute.none)
    dp.register_callback_query_handler(next_question, text='pass', state=StatesDispute.diary)
    dp.register_callback_query_handler(dispute_rules, text='rules', state=StatesDispute.none)
    dp.register_callback_query_handler(return_reports, text='Thanks1', state=StatesDispute.none)
    dp.register_callback_query_handler(awards, text='bonuses', state=StatesDispute.none)
    dp.register_callback_query_handler(return_reports, text='return_to_reports', state=StatesDispute.none)
    dp.register_callback_query_handler(promo_code_awards, text='1promo_code1', state=StatesDispute.none)
    dp.register_callback_query_handler(awards, text='back_awards', state=StatesDispute.none)
    dp.register_callback_query_handler(my_promocode, text='user_promocode', state=StatesDispute.none)
    dp.register_callback_query_handler(dispute_awards, text='dispute_award', state=StatesDispute.none)
    dp.register_callback_query_handler(deposit_button, text='deposit', state=StatesDispute.account)
    dp.register_callback_query_handler(withdraw_deposit, text='withdrawal_deposit', state=StatesDispute.account)
    dp.register_callback_query_handler(change_timezone, text='change_timezone', state=StatesDispute.account)
    dp.register_callback_query_handler(return_account, text='cancel_change_name', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 10', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 9:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 9', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 8', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 7', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 6', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 5', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 4', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 3:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 3', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 2', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='— 1', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+0', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+1', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+2', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+3', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+3:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+4', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+4:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+5', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+5:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+5:45', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+6', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+6:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+7', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+8', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+8:45', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+9', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+9:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+10', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+10:30', state=StatesDispute.account)
    dp.register_callback_query_handler(new_time_zone, text='+11', state=StatesDispute.account)
    dp.register_callback_query_handler(support_button, text='support', state=StatesDispute.account)
    dp.register_callback_query_handler(new_support_question, text='send_new_support', state=StatesDispute.account)
    dp.register_callback_query_handler(recieved_video, text='send_video', state=StatesDispute.video)
    dp.register_callback_query_handler(recieved_video, text='send_video', state=StatesDispute.video_note)
