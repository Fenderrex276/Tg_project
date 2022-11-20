from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile

from branches.confirm_dispute.states import Promo
from branches.dispute_with_friend.keyboards import *
from branches.dispute_with_friend.messages import *
from branches.dispute_with_friend.states import Form


async def test_of_will(call: types.CallbackQuery):
    await Form.none.set()

    photo = InputFile("media/volya/volya.jpg")
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=test_selection_keyboard,
                              caption="")
    #    await call.message.edit_text(text=just_do_it_m, reply_markup=test_selection_keyboard)
    await call.answer()


async def return_main_message(call: types.CallbackQuery):
    await Form.none.set()
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption="",
                                        reply_markup=test_selection_keyboard)
    await call.answer()


async def back_main_message(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    print(v['id_to_delete'])
    photo = InputFile("media/volya/volya.jpg")
    print("id FUCK", call.message.message_id)
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.delete_message(call.message.chat.id, v['id_to_delete'])

    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=test_selection_keyboard,
                              caption="")
    #    await call.message.edit_text(text=just_do_it_m, reply_markup=test_selection_keyboard)
    await call.answer()


async def back_message(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text=dispute_choice_msg, reply_markup=thirty_days_keyboard)
    await call.answer()


async def smoking_drink_drugs(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'id_to_delete': call.message.message_id})

    # await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.edit_reply_markup(reply_markup=drink_keyboard)
    await call.answer()


async def go_to_gym(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'id_to_delete': call.message.message_id})

    await call.message.edit_reply_markup(reply_markup=lose_weight_keyboard)
    await call.answer()


async def teach_something(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'id_to_delete': call.message.message_id})

    await call.message.edit_reply_markup(reply_markup=teach_something_keyboard)
    await call.answer()


async def quit_alcohol(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=quit_alcohol_msg)
    video = InputFile("media/videos/alcohol.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_alcohol_keyboard)
    await call.answer()


async def update_disput_choice(call: types.CallbackQuery, state: FSMContext):
    await Form.none.set()

    photo = InputFile("media/volya/volya.jpg")

    v = await state.get_data()
    print(v)
    print(call.message.message_id)
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    #    await call.bot.delete_message(call.message.chat.id, v['id_to_delete'])
    tmp_msg = ''
    tmp_keyboard = types.InlineKeyboardMarkup
    video = InputFile
    if v['action'] == 'alcohol':
        tmp_msg = quit_alcohol_msg
        tmp_keyboard = confirm_alcohol_keyboard
        video = InputFile("media/videos/alcohol.mp4")
    elif v['action'] == 'drugs':
        tmp_msg = quit_drugs_msg
        tmp_keyboard = confirm_drugs_keyboard
        video = InputFile("media/videos/drugs.mp4")
    elif v['action'] == 'smoking':
        tmp_msg = quit_smoking_msg
        tmp_keyboard = confirm_smoking_keyboard
        video = InputFile("media/videos/smoke.mp4")
    elif v['action'] == 'gym':
        tmp_msg = go_to_gym_msg
        tmp_keyboard = confirm_gym_keyboard
        video = InputFile("media/videos/gym.mp4")
    elif v['action'] == 'weight':
        tmp_msg = lose_weight_msg
        tmp_keyboard = confirm_lose_weight_keyboard
        video = InputFile("media/videos/weight.mp4")
    elif v['action'] == 'morning':
        tmp_msg = early_morning_msg
        tmp_keyboard = confirm_early_morning_keyboard
        video = InputFile("media/videos/morning.mp4")
    elif v['action'] == 'language':
        tmp_msg = teach_other_language_msg
        tmp_keyboard = confirm_other_language
        video = InputFile("media/videos/language.mp4")
    elif v['action'] == 'money':
        tmp_msg = more_money_msg
        tmp_keyboard = confirm_more_money_keyboard
        video = InputFile("media/videos/bank.mp4")
    elif v['action'] == 'food':
        tmp_msg = cook_helthy_food_msg
        tmp_keyboard = confirm_healthy_food_keyboard
        video = InputFile("media/videos/food.mp4")
    elif v['action'] == 'programming':
        tmp_msg = learn_programming_msg
        tmp_keyboard = confirm_programming_keyboard
        video = InputFile("media/videos/programming.mp4")
    elif v['action'] == 'instruments':
        tmp_msg = play_instruments_msg
        tmp_keyboard = confirm_play_instruments_keyboard
        video = InputFile("media/videos/piano.mp4")
    elif v['action'] == 'painting':
        tmp_msg = learn_painting_msg
        tmp_keyboard = confirm_painting_keyboard
        video = InputFile("media/videos/painting.mp4")

    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo,
                              caption=tmp_msg, parse_mode=ParseMode.MARKDOWN)

    await state.update_data({'id_to_delete': call.message.message_id + 1})
    if v['action'] == 'money':
        await call.bot.send_video(call.message.chat.id, video, reply_markup=tmp_keyboard)
    else:
        await call.bot.send_video_note(call.message.chat.id, video, reply_markup=tmp_keyboard)
    await call.answer()


async def quit_smoking(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=quit_smoking_msg)
    video = InputFile("media/videos/smoke.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_smoking_keyboard)
    await call.answer()


async def quit_drugs(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=quit_drugs_msg)
    video = InputFile("media/videos/drugs.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_smoking_keyboard)
    await call.answer()


async def go_gym(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=go_to_gym_msg)
    video = InputFile("media/videos/gym.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_gym_keyboard)
    await call.answer()


async def lose_weight(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=lose_weight_msg)
    video = InputFile("media/videos/weight.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_lose_weight_keyboard)
    await call.answer()


async def early_morning(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'id_to_delete': call.message.message_id})

    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=early_morning_msg)
    video = InputFile("media/videos/morning.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_early_morning_keyboard)
    # await call.message.answer(text=early_morning_msg, parse_mode=ParseMode.MARKDOWN,
    #    reply_markup=confirm_early_morning_keyboard)
    await call.answer()


async def teach_other_language(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'id_to_delete': call.message.message_id})

    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=teach_other_language_msg)

    video = InputFile("media/videos/language.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_other_language)
    await call.answer()


async def more_money(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'id_to_delete': call.message.message_id})

    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=more_money_msg)

    video = InputFile("media/videos/bank.mp4")
    await call.bot.send_video(call.message.chat.id, video, reply_markup=confirm_more_money_keyboard)
    await call.answer()


async def cook_healthy_food(call: types.CallbackQuery, state: FSMContext):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=cook_helthy_food_msg)

    video = InputFile("media/videos/food.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_healthy_food_keyboard)
    await call.answer()


async def learn_programming(call: types.CallbackQuery):
    # bot = call.bot
    # await bot.send_message()

    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=learn_programming_msg)

    video = InputFile("media/videos/programming.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_programming_keyboard)
    await call.answer()


async def play_instruments(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=play_instruments_msg)

    video = InputFile("media/videos/piano.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_play_instruments_keyboard)
    await call.answer()


async def learn_painting(call: types.CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                        parse_mode=ParseMode.MARKDOWN,
                                        message_id=call.message.message_id,
                                        caption=learn_painting_msg)

    video = InputFile("media/videos/painting.mp4")
    await call.bot.send_video_note(call.message.chat.id, video, reply_markup=confirm_painting_keyboard)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(test_of_will, text='thirty_days', state="*")

    dp.register_callback_query_handler(back_message, text='back_full_menu', state=Form.none)
    dp.register_callback_query_handler(return_main_message, text='back_quit_menu', state=Form.none)
    dp.register_callback_query_handler(back_main_message, text='return_main', state=Form.none)

    dp.register_callback_query_handler(smoking_drink_drugs, text='quit_something', state=Form.none)
    dp.register_callback_query_handler(go_to_gym, text='sport_lose_weight', state=Form.none)
    dp.register_callback_query_handler(teach_something, text='study_new', state=Form.none)

    dp.register_callback_query_handler(quit_alcohol, text='quit_drink', state=Form.none)

    dp.register_callback_query_handler(quit_smoking, text='quit_smoking', state=Form.none)
    dp.register_callback_query_handler(quit_drugs, text='quit_drugs', state=Form.none)

    dp.register_callback_query_handler(go_gym, text='gym', state=Form.none)
    dp.register_callback_query_handler(lose_weight, text='lose_weight', state=Form.none)

    dp.register_callback_query_handler(early_morning, text='early_morning', state="*")
    #    dp.register_callback_query_handler(early_morning1, text='early_morning1', state=Promo.input_promo)
    dp.register_callback_query_handler(teach_other_language, text='other_language', state=Form.none)
    #    dp.register_callback_query_handler(teach_other_language1, text='other_language1', state=Promo.input_promo)
    dp.register_callback_query_handler(more_money, text='more_money', state="*")
    #    dp.register_callback_query_handler(more_money1, text='more_money1', state=Promo.input_promo)

    dp.register_callback_query_handler(cook_healthy_food, text='healthy_food', state=Form.none)
    #    dp.register_callback_query_handler(cook_healthy_food1, text='healthy_food1', state=Promo.input_promo)
    dp.register_callback_query_handler(learn_programming, text='programming', state=Form.none)
    #    dp.register_callback_query_handler(learn_programming1, text='programming1', state=Promo.input_promo)
    dp.register_callback_query_handler(play_instruments, text='learn_play', state=Form.none)
    dp.register_callback_query_handler(learn_painting, text='painting', state=Form.none)

    dp.register_callback_query_handler(smoking_drink_drugs, text='back_drink_smoke_drugs', state=Promo.input_promo)
    dp.register_callback_query_handler(go_to_gym, text='sport_lose_weight', state=Promo.input_promo)

    dp.register_callback_query_handler(update_disput_choice, text='edit_disput1', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput2', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput3', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput4', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput5', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput6', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput7', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput8', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput9', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput10', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput11', state="*")
    dp.register_callback_query_handler(update_disput_choice, text='edit_disput12', state="*")
