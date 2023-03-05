from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from client.branches.confirm_dispute.messages import *
from client.branches.confirm_dispute.states import Promo
from client.branches.dispute_with_friend.states import Form
from client.tasks import reminder_scheduler_add_job, change_period_task_info
from utils import get_date_to_start_dispute, buttons_timezone


async def choice_alcohol(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='alcohol')
    await call.message.answer(text=alcohol_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_alcohol_keyboard,
                              disable_web_page_preview=True)

    await call.answer()


async def choice_smoking(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='smoking')
    await call.message.answer(text=smoking_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_alcohol_keyboard,
                              disable_web_page_preview=True)
    await call.answer()


async def choice_drugs(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='drugs')
    await call.message.answer(text=drugs_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_alcohol_keyboard,
                              disable_web_page_preview=True)
    await call.answer()


async def choice_gym(call: types.CallbackQuery, state: FSMContext):
    # print(call.message.text)
    await Promo.choose_dispute.set()
    await state.update_data(action='gym')

    await call.message.answer(text=gymm_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_gym_keyboard)
    await call.answer()


async def choice_lose_weight(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='weight')

    await call.message.answer(text=weight_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_gym_keyboard)
    await call.answer()


async def choice_early_morning(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='morning')

    await call.message.answer(text=morning_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_morning_keyboard)
    await call.answer()


async def choice_other_language(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='language')

    await call.message.answer(text=language_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_language_keyboard)
    await call.answer()


async def choice_more_money(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='money')
    await call.message.answer(text=money_msg2)
    await call.message.answer(text=money_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_more_money_keyboard)
    await call.answer()


async def choice_healthy_food(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='food')

    await call.message.answer(text=healthy_food_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_food_keyboard)
    await call.answer()


async def choice_programming(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='programming')

    await call.message.answer(text=programming_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_programming_keyboard)
    await call.answer()


async def choice_instruments(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action="instruments")

    await call.message.answer(text=instruments_msg2)
    await call.message.answer(text=instruments_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_instruments_keyboard)

    await call.answer()


async def choice_painting(call: types.CallbackQuery, state: FSMContext):
    await Promo.choose_dispute.set()
    await state.update_data(action='painting')

    await call.message.answer(text=painting_msg, parse_mode=ParseMode.MARKDOWN,
                              reply_markup=really_confirm_painting_keyboard)
    await call.answer()


async def monday_or_after_tomorrow(call: types.CallbackQuery, state: FSMContext):
    # print(call.data)
    await state.update_data(additional_action=call.data)

    await call.message.edit_text(text=monday_or_later_msg, reply_markup=select_day_keyboard)
    await call.answer()


async def recieved_date(call: types.CallbackQuery, state: FSMContext):
    await Promo.input_promo.set()
    await state.update_data(start_disput=call.data)
    await call.message.edit_text(text=promo_code_msg, reply_markup=no_promo_code_keyboard)
    await call.answer()


async def geo_position(call: types.CallbackQuery, state: FSMContext):
    await Promo.geo_position.set()
    await state.update_data(promocode='0')
    await call.message.answer(text=geo_position_msg, reply_markup=choose_time_zone_keyboard)
    # await call.message.answer(text=geo_position_msg, reply_markup=send_geo_position_keyboard)
    await call.answer()


async def set_geo_position(call: types.CallbackQuery, state: FSMContext):
    from client.initialize import dp

    await state.update_data(timezone=call.data, name=call.from_user.first_name)

    tmp_msg = f"Установлен часовой пояс {call.data} UTC"
    await call.message.answer(text=tmp_msg)
    variant = await state.get_data()

    is_change_timezone = variant.get('is_change_timezone', None)

    if is_change_timezone:
        await change_period_task_info(call.from_user.id, call.data)
    # if User.objects.filter(user_id=call.from_user.id).exists():
    #     #print("TYTYTYTYTYTYYTYTYTYTYT")  # SIMA TODO Сделать логику смены TZ из настроек профиля игрока
    #     await change_periodic_tasks(call.from_user.id, call.data)
    else:
        await reminder_scheduler_add_job(dp, call.data, "reminder", call.from_user.id, 1, notification_hour=10,
                                         notification_min=0)

    future_date = get_date_to_start_dispute(call.message.date, variant['start_disput'], call.data)
    photo, choice_msg, tmp_keyboard = get_timezone_msg(future_date, variant)

    await call.message.answer_photo(photo=photo, caption=choice_msg, reply_markup=tmp_keyboard,
                                    parse_mode=ParseMode.MARKDOWN_V2)
    await state.update_data({'id_to_delete': call.message.message_id})
    await Promo.next()
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choice_alcohol, text='select_quit_alcohol', state=Form.none)
    dp.register_callback_query_handler(choice_smoking, text='select_quit_smoking', state=Form.none)
    dp.register_callback_query_handler(choice_drugs, text='select_quit_drugs', state=Form.none)
    dp.register_callback_query_handler(choice_gym, text='select_go_gym', state=Form.none)
    dp.register_callback_query_handler(choice_lose_weight, text='select_lose_weight', state=Form.none)

    dp.register_callback_query_handler(choice_early_morning, text='select_early_morning', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='five_am', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='six_am', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='seven_am', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='eight_am', state=Promo.choose_dispute)

    dp.register_callback_query_handler(choice_other_language, text='select_other_language', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='english', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='chinese', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='spanish', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='arabian', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='italian', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='french', state=Promo.choose_dispute)

    dp.register_callback_query_handler(choice_more_money, text='select_more_money', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='hundred', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='three_hundred', state=Promo.choose_dispute)

    dp.register_callback_query_handler(choice_healthy_food, text='select_healthy_food', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='agree_food', state=Promo.choose_dispute)

    dp.register_callback_query_handler(choice_programming, text='select_programming', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='agree_programming', state=Promo.choose_dispute)

    dp.register_callback_query_handler(choice_instruments, text='select_play_instruments', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='piano', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='guitar', state=Promo.choose_dispute)

    dp.register_callback_query_handler(choice_painting, text='select_painting', state=Form.none)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='pad', state=Promo.choose_dispute)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='hand', state=Promo.choose_dispute)

    dp.register_callback_query_handler(monday_or_after_tomorrow, text='next_step_two', state=Promo.choose_dispute)

    dp.register_callback_query_handler(recieved_date, text='select_monday', state=Promo.choose_dispute)
    dp.register_callback_query_handler(recieved_date, text='select_after_tomorrow', state=Promo.choose_dispute)

    dp.register_callback_query_handler(geo_position, text='next_step_three', state=Promo.input_promo)
    buttons_timezone(dp=dp, func=set_geo_position, current_state=Promo.geo_position)
