from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from client.branches.confirm_dispute.states import Promo
from client.branches.pay.keyboards import *
from client.branches.pay.messages import *
from client.branches.pay.states import PayStates
from db.models import Users
from client.tasks import del_scheduler, scheduler_add_job
from client.initialize import dp


async def choose_sum_to_pay(call: types.CallbackQuery):
    await PayStates.pay.set()

    del_scheduler(f'{call.from_user.id}_reminder')

    scheduler_add_job(dp, 'reminder', call.from_user.id, 2)
    await call.message.answer(text=deposit_msg, reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="*Выбери комфортную сумму*", parse_mode=ParseMode.MARKDOWN_V2,
                              reply_markup=choose_sum_keyboard)
    await call.answer()


async def check_sum(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(deposit=call.data)
    await PayStates.none.set()
    await call.message.edit_text(text=application_for_payment_msg, reply_markup=get_banking_detials_keyboard,
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()
    del_scheduler(f'{call.from_user.id}_reminder')

    scheduler_add_job(dp, 'reminder', call.from_user.id, 3)


async def other_sum_to_pay(call: types.CallbackQuery):
    await PayStates.input_sum.set()
    await call.message.answer(text=other_sum_msg, reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def get_bank_details(call: types.CallbackQuery, state: FSMContext):
    money = await state.get_data()
    bank_details_msg = ("Заявка #TG2802\n Переведи точную сумму:\n"
                        f" {money['deposit']} ₽\n По реквизитам карты:\n"
                        " 4276 4000 4033 9999\n (без коммента)")
    await call.message.edit_text(text=bank_details_msg, reply_markup=confirm_deposit_payed_keyboard)
    await call.answer()
    del_scheduler(f'{call.from_user.id}_reminder')

    scheduler_add_job(dp, 'reminder', call.from_user.id, 4)
    # TODO Куда улетает запрос после жмяка на Подтвердить


async def successful_payment(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    print(v)

    success_payment_msg = ("Поздравляем 🎉 ты уже в шаге от цели. Заявка #TG2802 успешно оплачена.\n\n"
                           f" 🔥 Твой депозит пополнен на {v['deposit']} ₽ и заморожен до конца пари — соблюдай "
                           f"условия каждый"
                           " из 30 дней и сохрани депозит, всё зависит только от тебя")
    await call.message.edit_text(text=success_payment_msg, reply_markup=go_keyboard)
    await call.answer()
    del_scheduler(f'{call.from_user.id}_reminder')

    scheduler_add_job(dp, 'reminder', call.from_user.id, 5)


async def start_current_disput(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
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

    start_current_disput_msg = (f"👋 Привет, {call.from_user.first_name},"
                                f" заверши свою подготовку к цели и начни путь героя.\n\n"
                                "*Твоя цель:*\n"
                                f"{purpose}\n"
                                f"🧊 Депозит: {data['deposit']} ₽ \n\n"
                                "*Условия на 30 дней*\n"
                                f"{video_with_code}\n"
                                f"⏳ Отправлять в бот до {time_before}\n\n"
                                "До победы осталось 30 дней\n"
                                f"Право на ошибку: {data['promocode']}")

    start_d = ""
    if data['start_disput'] == "select_after_tomorrow":
        start_d = "tomorrow"
    elif data['start_disput'] == "select_monday":
        start_d = "monday"
    deposit = int(data['deposit'].replace(" ", ""))

    await Users.objects.acreate(user_id=call.from_user.id,
                                user_name=call.from_user.first_name,
                                action=data['action'],
                                additional_action=data['additional_action'],
                                start_disput=start_d,
                                deposit=deposit,
                                count_days=30)

    await call.message.edit_text(text=start_current_disput_msg, reply_markup=next_step_keyboard,
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_sum_to_pay, text='make_deposit', state=Promo.none)
    dp.register_callback_query_handler(other_sum_to_pay, text='other_sum', state=PayStates.pay)
    dp.register_callback_query_handler(check_sum, text='15 000', state=PayStates.pay)
    dp.register_callback_query_handler(check_sum, text='30 000', state=PayStates.pay)
    dp.register_callback_query_handler(check_sum, text='50 000', state=PayStates.pay)
    dp.register_callback_query_handler(check_sum, text='100 000', state=PayStates.pay)
    dp.register_callback_query_handler(get_bank_details, text='get_details', state=PayStates.none)
    dp.register_callback_query_handler(successful_payment, text='access', state=PayStates.none)
    dp.register_callback_query_handler(start_current_disput, text='go_disput', state=PayStates.none)
