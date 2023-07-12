from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import secrets
from client.branches.confirm_dispute.states import Promo
from client.branches.pay.keyboards import *
from client.branches.pay.messages import *
from client.branches.pay.states import PayStates
from db.models import User
from client.tasks import del_scheduler, reminder_scheduler_add_job
from client.initialize import dp
from client.branches.thirty_days_dispute.keyboards import menu_keyboard
from client.branches.training.states import Video


async def choose_sum_to_pay(call: types.CallbackQuery, state: FSMContext):
    await PayStates.first_m.set()

    del_scheduler(f'{call.from_user.id}_reminder', 'client')
    redis_data = await state.get_data()

    await reminder_scheduler_add_job(dp, redis_data['timezone'], 'reminder', call.from_user.id, 2, notification_hour=10,
                                     notification_min=0)

    await call.message.answer(text=deposit_msg, reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="*Выбери комфортную сумму*", parse_mode=ParseMode.MARKDOWN_V2,
                              reply_markup=choose_sum_keyboard)
    await call.answer()


async def check_sum(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(deposit=call.data)
    await PayStates.second_m.set()
    await call.message.edit_text(text=application_for_payment_msg, reply_markup=get_banking_detials_keyboard,
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()
    del_scheduler(f'{call.from_user.id}_reminder', 'client')

    redis_data = await state.get_data()
    await reminder_scheduler_add_job(dp, redis_data['timezone'], 'reminder', call.from_user.id, 3, notification_hour=10,
                                     notification_min=0)


async def other_sum_to_pay(call: types.CallbackQuery):
    await PayStates.input_sum.set()
    await call.message.answer(text=other_sum_msg, reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def get_bank_details(call: types.CallbackQuery, state: FSMContext):
    await PayStates.third_m.set()
    money = await state.get_data()
    bank_details_msg = ("Заявка #TG2802\n Переведи точную сумму:\n"
                        f" {money['deposit']} ₽\n По реквизитам карты:\n"
                        " 4276 4000 4033 9999\n (без коммента)")
    await call.message.edit_text(text=bank_details_msg, reply_markup=confirm_deposit_payed_keyboard)
    await call.answer()
    del_scheduler(f'{call.from_user.id}_reminder', 'client')

    redis_data = await state.get_data()
    await reminder_scheduler_add_job(dp, redis_data['timezone'], 'reminder', call.from_user.id, 4, notification_hour=10,
                                     notification_min=0)


async def successful_payment(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    await PayStates.none.set()
    await call.message.answer(text="Поздравляем 🎉 ты уже в шаге от цели. Заявка #TG2802 успешно оплачена.\n\n",
                              reply_markup=menu_keyboard)
    n_d = 30
    if v['count_days'] == 3:
        n_d = 3
    success_payment_msg = (f" 🔥 Твой депозит пополнен на {v['deposit']} ₽ и заморожен до конца пари — соблюдай "
                           f"условия каждый"
                           f" из {n_d} и сохрани депозит, всё зависит только от тебя")

    await call.message.answer(text=success_payment_msg, reply_markup=go_keyboard)
    await call.answer()

    redis_data = await state.get_data()
    del_scheduler(f'{call.from_user.id}_reminder', 'client')
    start_d = "0"
    if redis_data['start_disput'] == "select_after_tomorrow":
        start_d = "tomorrow"
    elif redis_data['start_disput'] == "select_monday":
        start_d = "monday"
    deposit = int(redis_data['deposit'].replace(" ", ""))

    mistake = 0
    if redis_data['promocode'] != '0':
        mistake = 1

    try:

        user = await User.objects.aget(user_id=call.from_user.id)
        user.user_name = call.from_user.first_name
        user.action = redis_data['action']
        user.additional_action = redis_data['additional_action']
        user.start_disput = "0"
        user.promocode_user = secrets.token_hex(nbytes=5)
        user.promocode_from_friend = redis_data['promocode']
        user.count_days = redis_data['count_days']
        user.timezone = redis_data['timezone']
        user.deposit = deposit
        user.count_mistakes = (2 + mistake)
        user.save()
    except User.DoesNotExist:

        await User.objects.acreate(user_id=call.from_user.id,
                                   chat_id=call.message.chat.id,
                                   user_name=call.from_user.first_name,
                                   action=redis_data['action'],
                                   additional_action=redis_data['additional_action'],
                                   start_disput="0",
                                   deposit=deposit,
                                   promocode_user=secrets.token_hex(nbytes=5),
                                   promocode_from_friend=redis_data['promocode'],
                                   count_days=redis_data['count_days'],
                                   timezone=redis_data['timezone'],
                                   count_mistakes=(2 + mistake))

    await state.update_data(name=call.from_user.first_name)

    await reminder_scheduler_add_job(dp, redis_data['timezone'], 'send_test_period_reminder', call.from_user.id,
                                     notification_hour=10,
                                     notification_min=0)


async def start_current_disput(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    start_current_disput_msg = starting_message_dispute(data, call.from_user.first_name)

    await call.message.edit_text(text=start_current_disput_msg, reply_markup=next_step_keyboard,
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_sum_to_pay, text='make_deposit', state=Promo.none)
    dp.register_callback_query_handler(choose_sum_to_pay, text='start_pay_state', state=Promo.none)
    dp.register_callback_query_handler(choose_sum_to_pay, text='choose_current_sum', state=PayStates.first_m)
    dp.register_callback_query_handler(other_sum_to_pay, text='other_sum', state=PayStates.first_m)
    dp.register_callback_query_handler(check_sum, text='15 000', state=PayStates.first_m)
    dp.register_callback_query_handler(check_sum, text='30 000', state=PayStates.first_m)
    dp.register_callback_query_handler(check_sum, text='50 000', state=PayStates.first_m)
    dp.register_callback_query_handler(check_sum, text='100 000', state=PayStates.first_m)
    dp.register_callback_query_handler(get_bank_details, text='get_pay_details', state=PayStates.second_m)
    dp.register_callback_query_handler(get_bank_details, text='get_details', state=PayStates.second_m)
    dp.register_callback_query_handler(successful_payment, text='access', state=PayStates.third_m)
    dp.register_callback_query_handler(successful_payment, text='confirm_deposit', state=PayStates.third_m)
    dp.register_callback_query_handler(start_current_disput, text='go_disput', state=PayStates.none)
    dp.register_callback_query_handler(start_current_disput, text='start_current_dispute', state=PayStates.none)
    dp.register_callback_query_handler(successful_payment, text='make_deposit', state=Promo.blogger)
