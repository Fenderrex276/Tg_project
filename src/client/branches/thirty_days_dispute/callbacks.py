import random
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from .diary import questions
from .keyboards import *
from .states import StatesDispute, NewReview


from db.models import RoundVideo, User
from ..confirm_dispute.keyboards import choose_time_zone_keyboard
from ..dispute_with_friend.messages import personal_goals_msg
from client.tasks import del_scheduler, change_period_task_info, reminder_scheduler_add_job
from client.initialize import dp
from client.tasks import change_period_task_info
from utils import buttons_timezone
from .messages import video_text, get_message_video


async def begin_dispute(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.none.set()
    await state.update_data(is_deleted=-1)

    data = await state.get_data()
    n_d = 30
    if data['is_blogger'] is True:
        n_d = 3
    recieve_message = video_text(data, n_d, data['deposit'])

    await call.message.answer_photo(photo=InputFile(recieve_message[0]), caption=recieve_message[1],
                                    reply_markup=menu_keyboard,
                                    parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def reports(call: types.CallbackQuery, state: FSMContext):
    main_photo = InputFile("client/media/Disput Bot-2/Default.png")
    try:

        user = User.objects.get(user_id=call.from_user.id)
    except User.DoesNotExist:
        print(f'Такого пользователя с id:{call.from_user.id} не существует')
        return

    current_video = RoundVideo.objects.filter(user_tg_id=call.from_user.id,
                                              type_video=RoundVideo.TypeVideo.archive).last()

    redis_data = await state.get_data()
    if redis_data['is_blogger'] is True:

        if current_video.status == "good" and user.count_days != 3:  # TODO Исправить косяк. Описал в ТГ

            if user.count_mistakes == 3 and current_video.n_day == 28:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{1}.png")
            elif user.count_mistakes == 3 and current_video.n_day != 0:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days - 27}-{1}.png")
            elif user.count_mistakes == 2 and current_video.n_day != 0:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days - 27}.png")
            elif user.count_days == 0 and user.count_mistakes != 0:
                main_photo = InputFile("client/media/days_of_dispute/days/BLOGER WIN.png")
                await state.update_data(is_blogger=False)
                # TODO Отправка уведомлений о повторной игре
                # TODO RUS Предложить отзывы если он победил
                await reminder_scheduler_add_job(dp, user.timezone, 'send_reminder_after_end', call.from_user.id,
                                                 notification_hour=10, notification_min=0)

        elif current_video.status == "bad" and user.count_days != 3:

            if user.count_mistakes == 2 and current_video.n_day == 28:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{1}-{2}.png")
            elif user.count_mistakes == 2 and user.promocode_from_friend != '0':
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days - 27}-{3}.png")
            elif user.count_mistakes == 1:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days - 27}-{2}.png")
            elif user.count_mistakes == 0:
                main_photo = InputFile(f"client/media/days_of_dispute/days/BLOGER SAD FINISH.png")
                await state.update_data(is_blogger=False)
    else:

        if current_video.status == "good" and user.count_days != 30:

            if (user.count_mistakes == 3 or (
                    user.count_mistakes == 2 and user.promocode_from_friend == '0')) and current_video.n_day == 1:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{1}.png")
            elif user.count_mistakes == 3 or (
                    user.count_mistakes == 2 and user.promocode_from_friend == '0') and current_video.n_day != 0:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days}-{1}.png")
            elif (user.count_mistakes == 2 or (
                    user.count_mistakes == 1 and user.promocode_from_friend == '0')) and current_video.n_day != 0:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days}.png")
            elif user.count_days == 0 and user.count_mistakes != 0:
                main_photo = InputFile("client/media/days_of_dispute/days/USER WIN.png")
                # TODO Отправка уведомлений о повторной игре
                # TODO RUS Предложить отзывы если он победил

        elif current_video.status == "bad" and user.count_days != 30:

            if user.count_mistakes == 2 and current_video.n_day == 1 and user.promocode_from_friend != '0':
                main_photo = InputFile(f"client/media/days_of_dispute/days/{1}-{2}.png")
            elif user.count_mistakes == 1 and current_video.n_day == 1 and user.promocode_from_friend == '0':
                main_photo = InputFile(f"client/media/days_of_dispute/days/{1}-{1}.png")
            elif user.count_mistakes == 2 and user.promocode_from_friend != '0':
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days}-{3}.png")

            elif user.count_mistakes == 1:
                main_photo = InputFile(f"client/media/days_of_dispute/days/{30 - user.count_days}-{2}.png")
            elif user.count_mistakes == 0:
                main_photo = InputFile(f"client/media/days_of_dispute/days/USER SAD FINISH.png")

    cur_state = await state.get_state()
    if cur_state not in StatesDispute.states_names:
        return
    else:
        await StatesDispute.reports.set()

    await state.update_data(is_deleted=-1)

    if user.count_mistakes == 0:

        await state.update_data(deposit=0)
        user.count_days = 0
        user.deposit = 0
        user.save()
        await call.message.answer_photo(InputFile(f"client/media/days_of_dispute/days/USER SAD FINISH.png"),
                                        reply_markup=new_menu_keyboard)
        await call.message.answer(text="Выберите следующее действие:", reply_markup=end_game_keyboard)
        await reminder_scheduler_add_job(dp, user.timezone, 'send_reminder_after_end', call.from_user.id,
                                         notification_hour=10, notification_min=0)
    elif user.count_days == 0 and user.count_mistakes != 0:
        await call.message.answer_photo(InputFile(f"client/media/days_of_dispute/days/USER WIN.png"),
                                        reply_markup=new_menu_keyboard)
        await call.message.answer(text="Выберите следующее действие:", reply_markup=end_game_keyboard)
        await reminder_scheduler_add_job(dp, user.timezone, 'send_reminder_after_end', call.from_user.id,
                                         notification_hour=10, notification_min=0)
    else:
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
    current_state = await state.get_state()
    msg = "💬 Введи своё новое имя:"

    await call.message.edit_text(text=msg)
    if current_state in StatesDispute.states_names:
        await StatesDispute.change_name.set()
    await call.answer()


async def check_report(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.new_report.set()
    # await state.update_data(current_message=1, id_to_delete=call.message.message_id+1)

    try:
        user_videos = RoundVideo.objects.filter(user_tg_id=call.from_user.id,
                                                chat_tg_id=call.message.chat.id,
                                                type_video=RoundVideo.TypeVideo.dispute,
                                                tg_id="")
        data = await state.get_data()
        print("COUNT VIDEOS WITHOUT ID FILE", len(user_videos))

        user_video = await RoundVideo.objects.filter(user_tg_id=call.from_user.id,
                                                     chat_tg_id=call.message.chat.id,
                                                     type_video=RoundVideo.TypeVideo.dispute
                                                     ).alast()

        # user_video = await RoundVideo.objects.aget(id_video=data['id_video_code'])
        if user_video.status == "" and user_video.tg_id is not None:
            tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."
            await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text='Назад',
                                           callback_data='Thanks1')))

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
        # ?????????????
        await call.message.edit_caption(caption='Твой новый код придёт в бот автоматически.',
                                        reply_markup=types.InlineKeyboardMarkup().add(
                                            types.InlineKeyboardButton(text='Назад',
                                                                       callback_data='Thanks1')))
    await call.answer()


async def recieved_video(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await StatesDispute.none.set()
    current_video = await RoundVideo.objects.filter(chat_tg_id=call.message.chat.id,
                                                    type_video=RoundVideo.TypeVideo.dispute,
                                                    id_video=data['id_video_code']).alast()
    current_video.tg_id = data['video_id']
    current_video.save()

    tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."
    await call.bot.send_video_note(video_note=data['video_id'], chat_id=-1001845655881)
    await call.message.answer(text=tmp_msg)
    await call.answer()


async def send_new_report_from_admin(call: types.CallbackQuery, state: FSMContext):
    # print(call.from_user.id, call.message.chat.id)
    new_video = await RoundVideo.objects.filter(user_tg_id=call.from_user.id,
                                                chat_tg_id=call.message.chat.id,
                                                type_video=RoundVideo.TypeVideo.dispute
                                                ).alast()

    print(new_video.id_video)

    # data = await state.get_data()

    await state.update_data(new_code=new_video.code_in_video, id_video_code=new_video.id_video)

    new_code = " ".join(list(new_video.code_in_video))
    user = await User.objects.filter(user_id=call.from_user.id).alast()

    temp_array = get_message_video({'action': user.action, 'additional_action': user.additional_action}, new_code)

    await call.message.answer(text=temp_array[0])

    if user.action == 'money':
        await StatesDispute.video.set()
        await call.message.answer_video(video=InputFile(temp_array[1]))
    else:
        await StatesDispute.video_note.set()
        await call.message.answer_video_note(video_note=InputFile(temp_array[1]))
    await call.answer()


async def diary_button(call: types.CallbackQuery, state: FSMContext):
    msg = ("📝 Дневник — это честный диалог "
           "с самим собой, со своим внутренним «Я» в интерактивной форме.\n\n"
           "Дневник подразумевает признание"
           "в чём-либо. Как известно, признание проблемы — первый шаг на пути "
           "к её решению.\n\n"
           "Бот будет отправлять вопросы, ты можешь дать свой ответ или пропустить вопрос. Твои ответы никуда не "
           "отправляются и "
           "остаются здесь, наедине с тобой.\n\n"
           "Перечитай и проанализируй их, посмотри на ситуации и себя со стороны и продолжай свой путь")

    await state.update_data(number_question=random.randint(0, 45))
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


async def admit_answer(call: types.CallbackQuery):
    await StatesDispute.diary.set()
    msg = "💬 Пиши всё, что придёт в голову:"
    await call.message.answer(text=msg)
    await call.answer()


async def next_question(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await random_question(call, state)


async def dispute_rules(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    start_time_dispute = ""
    array = ['alcohol', 'drugs', 'smoking', 'gym', 'weight', 'language', 'programming', 'paint', 'food',
             'instruments']
    user = await User.objects.aget(user_id=call.from_user.id)
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
    promocode = '0'
    if data['promocode'] != '0' and user.count_mistakes == 3:
        promocode = '1'

    tmp_msg = ("😇 Правила диспута\n\n"
               f"Мы принимаем твой репорт в этом диспуте в период с {start_time_dispute}\n\n"
               "Каждый день бот присылает уведомление со специальным кодом из четырёх цифр, "
               "который тебе необходимо произнести на видео, как в примере, и отправить в бот вовремя.\n\n"
               "👍 Если все ок, игра продолжится и"
               "вы сохраните свой депозит\n\n"
               "👎 Если правила спора нарушены, вы проиграете сначала "
               "20% депозита, а если это повторится — остальные 80%.\n\n"
               f"Право на ошибку: {promocode}")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='👍 Спасибо', callback_data='Thanks1')))
    await call.answer()


async def return_reports(call: types.CallbackQuery):
    await StatesDispute.reports.set()
    await call.message.edit_caption(caption="", reply_markup=report_keyboard)
    await call.answer()


async def awards(call: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == "StatesDispute:reports" or cur_state == "StatesDispute:bonuses":
        await StatesDispute.bonuses.set()
    else:
        return
    tmp_msg = ("👑 Бонусы — 0 ₽\n\n"
               "Выбери задание и зарабатывай дополнительные 💰 в свой депозит")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=awards_keyboard)
    await call.answer()


async def promo_code_awards(call: types.CallbackQuery):
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


async def my_promocode(call: types.CallbackQuery):
    print("PROMOCODE ENTER: ", call.message.message_id)
    return_keyboard = types.InlineKeyboardMarkup()
    return_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_promocode_rules'))
    user_promocode = await User.objects.filter(user_id=call.from_user.id).alast()
    await call.message.edit_caption(caption=f"`{user_promocode.promocode_user}`\nЗажми промо-код, чтобы скопировать",
                                    parse_mode=ParseMode.MARKDOWN, reply_markup=return_keyboard)

    await call.answer()


async def dispute_awards(call: types.CallbackQuery):
    tmp_msg = ("⭐️ Отправь свой лучший кружочек "
               "на ежемесячный конкурс DisputeAward.\n\n"

               "На твой пример смогут ровняться "
               "тысячи игроков, а ты заработаешь"
               "+5 000 ₽ к своему депозиту.\n\n"

               "Можно отправить только 1 видео / мес.")

    await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='👀 Выбрать', callback_data='choose_video_to_dispute_award'),
        types.InlineKeyboardButton(text='Назад', callback_data='return_to_bonuses')))
    await call.answer()


async def choose_video_to_contest(call: types.CallbackQuery, state: FSMContext):
    user = await User.objects.aget(user_id=call.from_user.id)
    tmp_msg = ""
    data = state.get_data()
    if user.count_days < 23 and data['is_blogger'] is False:
        tmp_msg = "Выбери видео..."
    else:
        tmp_msg = "Будет доступно только после 7 дней в игре"

    await call.message.edit_caption(caption=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data='return_to_awards')))


async def deposit_button(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(id_to_delete=call.message.message_id)
    user = await User.objects.aget(user_id=call.from_user.id)

    tmp_msg = (f"*💰 Депозит: {user.deposit} ₽*\n"
               f"{user.deposit} ₽ \+ 0 ₽ бонусов\n\n"
               "Твой депозит и бонусы заморожены в Диспуте до момента победы в споре и будут доступны для вывода "
               "или для начала следующей игры\n\n"
               "⚠️️ Бонусы отдельно без депозита не подлежат выводу\\.")
    dep_keyboard = types.InlineKeyboardMarkup()
    dep_keyboard.add(
        types.InlineKeyboardButton(text='Вывод 💰', callback_data='withdrawal_deposit'),
        types.InlineKeyboardButton(text='Личные 🎯️ цели', callback_data='personal_goals'))
    dep_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_account'))

    await call.message.edit_text(text=tmp_msg, reply_markup=dep_keyboard,
                                 parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()


async def personal_goals(call: types.CallbackQuery):
    await StatesDispute.personal_goals.set()
    photo = InputFile("client/media/volya/volya1.jpg")
    await call.message.answer_photo(photo=photo,
                                    caption=personal_goals_msg,
                                    reply_markup=types.InlineKeyboardMarkup().add(
                                        types.InlineKeyboardButton(text="Назад", callback_data="back_account")
                                    ))


async def return_to_account(call: types.CallbackQuery, state: FSMContext):
    await StatesDispute.account.set()

    user = await state.get_data()
    # await call.bot.delete_message(message_id=user['id_to_delete'], chat_id=call.message.chat.id)
    # await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)

    msg = (f"👋 *Привет, {user['name']}* \n\n"
           "Здесь ты можешь изменить своё имя, вывести выигранный депозит, "
           "изменить свой часовой пояс или написать свой вопрос в тех. "
           "поддержку через форму обратной связи.")

    await call.message.answer(text=msg, reply_markup=account_keyboard, parse_mode=ParseMode.MARKDOWN)


async def withdraw_deposit(call: types.CallbackQuery):
    user = await User.objects.filter(user_id=call.from_user.id).alast()

    tmp_msg = (f"🚩*До победы осталось {user.count_days} дней\.*\n\n"

               "Пройди свой Путь Героя и вывод твоего депозита на банковскую "
               "карту или в BTC станет доступен в этом окне")
    # TODO Доделать вывод депозита
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data='back_to_deposit')
    ),
                                 parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()


async def view_user_timezone(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tmp_msg = f"🌍 Установлен часовой пояс {data['timezone']} UTC"
    back_or_send_keyboard = types.InlineKeyboardMarkup()
    back_or_send_keyboard.add(types.InlineKeyboardButton(text='Изменить', callback_data='confirm_to_change_timezone'),
                              types.InlineKeyboardButton(text='Всё верно 👍', callback_data='cancel_edit_timezone'))
    await call.message.edit_text(text=tmp_msg, reply_markup=back_or_send_keyboard)


async def change_timezone(call: types.CallbackQuery, state: FSMContext):
    geo_position_msg = (
        "🌍 Укажи разницу во времени относительно UTC (Москва +3, Красноярск +7 и тд) или отправь в бот "
        "геопозицию (возьмем только часовой пояс)")

    # test_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # test_keyboard.add(types.KeyboardButton(text='Отправить гео 📍', request_location=True))
    #
    await call.message.answer(text=geo_position_msg, reply_markup=choose_time_zone_keyboard)
    current_state = await state.get_state()
    if current_state in StatesDispute.states_names:
        await StatesDispute.new_timezone.set()

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
    user = User.objects.filter(user_id=call.from_user.id).last()
    user.timezone = call.data
    user.save()
    tmp_msg = f"Установлен часовой пояс {call.data} UTC"
    await change_period_task_info(user.user_id, call.data)
    current_state = await state.get_state()
    if current_state in StatesDispute.states_names:
        await StatesDispute.none.set()
    await call.message.answer(text=tmp_msg, reply_markup=menu_keyboard)
    await call.answer()


async def support_button(call: types.CallbackQuery):
    tmp_msg = ("🆘 *Поддержка*\n\n"

               "Расскажи о технической ошибке, если столкнёшься с этим в процессе, и наши арбитры оперативно придут "
               "на помощь.\n\n"

               "Будем очень благодарны твоему опыту взаимодействия с ботом и в сложных случаях всегда будем на твоей "
               "стороне 🤝")

    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Сообщить о проблеме', callback_data='send_new_support'),
        types.InlineKeyboardButton(text='Назад', callback_data="cancel_change_name")),
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def new_support_question(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer(text='💬 Введи сообщение:')
    current_state = await state.get_state()
    if current_state in StatesDispute.states_names:
        await StatesDispute.new_question.set()

    await call.answer()


async def new_review(call: types.CallbackQuery):
    await NewReview.input_city.set()
    await call.message.answer(text="🌇 Напиши свой город:")


async def new_coment(call: types.CallbackQuery, state: FSMContext):
    await NewReview.input_review.set()
    await state.update_data(stars=call.data)

    await call.message.answer(text="💬 Напиши текст отзыва:")


async def sad_finish_after_test(call: types.CallbackQuery, state: FSMContext):
    try:

        user = User.objects.get(user_id=call.from_user.id)
    except User.DoesNotExist:
        print(f'Такого пользователя с id:{call.from_user.id} не существует')
        return
    await state.update_data(deposit=0)
    user.count_days = 0
    user.deposit = 0
    user.save()
    data = await state.get_data()

    image = InputFile(f"client/media/days_of_dispute/days/USER SAD FINISH.png")

    if data['is_blogger'] is True:
        image = InputFile(f"client/media/days_of_dispute/days/BLOGER SAD FINISH.png")

    await call.message.answer_photo(image, reply_markup=new_menu_keyboard)
    await call.message.answer(text="Выберите следующее действие:", reply_markup=end_game_keyboard)
    await reminder_scheduler_add_job(dp, user.timezone, 'send_reminder_after_end', call.from_user.id,
                                     notification_hour=10, notification_min=0)


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(begin_dispute, text='go_dispute', state="*")
    dp.register_callback_query_handler(reports, text='report', state=StatesDispute.none)

    dp.register_callback_query_handler(choose_name_button, text='change_name', state="*")
    dp.register_callback_query_handler(change_name, text='change_name_access', state="*")

    dp.register_callback_query_handler(check_report, text="send_new_report", state=StatesDispute.reports)
    dp.register_callback_query_handler(send_new_report_from_admin, text="send_dispute_report", state="*")

    dp.register_callback_query_handler(diary_button, text='diary', state=StatesDispute.none)
    dp.register_callback_query_handler(random_question, text='random_questions', state=StatesDispute.none)
    dp.register_callback_query_handler(admit_answer, text='admit', state=StatesDispute.none)
    dp.register_callback_query_handler(admit_answer, text='admit', state=StatesDispute.diary)
    dp.register_callback_query_handler(next_question, text='pass', state=StatesDispute.none)
    dp.register_callback_query_handler(next_question, text='pass', state=StatesDispute.diary)

    dp.register_callback_query_handler(dispute_rules, text='rules', state=StatesDispute.reports)
    dp.register_callback_query_handler(return_reports, text='Thanks1', state=StatesDispute.reports)

    dp.register_callback_query_handler(awards, text='bonuses', state=StatesDispute.reports)
    dp.register_callback_query_handler(awards, text='return_to_bonuses', state=StatesDispute.bonuses)

    dp.register_callback_query_handler(return_reports, text='Thanks1', state=StatesDispute.new_report)
    dp.register_callback_query_handler(return_reports, text='return_to_reports', state=StatesDispute.bonuses)
    dp.register_callback_query_handler(promo_code_awards, text='1promo_code1', state=StatesDispute.bonuses)
    dp.register_callback_query_handler(awards, text='back_awards', state=StatesDispute.bonuses)
    dp.register_callback_query_handler(promo_code_awards, text='back_to_promocode_rules', state=StatesDispute.bonuses)
    dp.register_callback_query_handler(my_promocode, text='user_promocode', state=StatesDispute.bonuses)

    dp.register_callback_query_handler(dispute_awards, text='dispute_award', state=StatesDispute.bonuses)
    dp.register_callback_query_handler(dispute_awards, text='return_to_awards', state=StatesDispute.bonuses)
    dp.register_callback_query_handler(choose_video_to_contest, text='choose_video_to_dispute_award',
                                       state=StatesDispute.bonuses)

    dp.register_callback_query_handler(deposit_button, text='deposit', state="*")
    dp.register_callback_query_handler(deposit_button, text='back_to_deposit', state="*")
    dp.register_callback_query_handler(withdraw_deposit, text='withdrawal_deposit', state="*")

    dp.register_callback_query_handler(view_user_timezone, text='change_timezone', state="*")
    dp.register_callback_query_handler(change_timezone, text='confirm_to_change_timezone', state="*")

    dp.register_callback_query_handler(return_account, text='cancel_change_name', state="*")
    dp.register_callback_query_handler(return_account, text='cancel_edit_timezone', state="*")
    dp.register_callback_query_handler(return_account, text='back_to_account', state="*")
    buttons_timezone(dp=dp, func=new_time_zone, current_state=StatesDispute.new_timezone)

    dp.register_callback_query_handler(support_button, text='support', state="*")

    dp.register_callback_query_handler(new_support_question, text='send_new_support', state="*")
    dp.register_callback_query_handler(new_support_question, text='send_new_support', state=StatesDispute.states)
    dp.register_callback_query_handler(recieved_video, text='send_video', state=StatesDispute.video)
    dp.register_callback_query_handler(recieved_video, text='send_video', state=StatesDispute.video_note)

    # dp.register_callback_query_handler(my_promocode, text='user_promocode', state=StatesDispute.promo_code)
    dp.register_callback_query_handler(personal_goals, text='personal_goals', state=StatesDispute.states)
    dp.register_callback_query_handler(return_to_account, text="back_account", state=StatesDispute.personal_goals)

    dp.register_callback_query_handler(reports, text='nice_god_job', state="*")
    dp.register_callback_query_handler(reports, text='try_again', state="*")
    dp.register_callback_query_handler(send_new_report_from_admin, text="send_new_video", state=StatesDispute.video)
    dp.register_callback_query_handler(send_new_report_from_admin, text="send_new_video",
                                       state=StatesDispute.video_note)

    dp.register_callback_query_handler(sad_finish_after_test, text='new_dispute_after_finish',
                                       state="*")  # на седьмой день, чел не прошел тест

    dp.register_callback_query_handler(new_review, text='new_review', state="*")
    dp.register_callback_query_handler(new_coment, text='one', state="*")
    dp.register_callback_query_handler(new_coment, text='two', state="*")
    dp.register_callback_query_handler(new_coment, text='three', state="*")
    dp.register_callback_query_handler(new_coment, text='four', state="*")
    dp.register_callback_query_handler(new_coment, text='five', state="*")
