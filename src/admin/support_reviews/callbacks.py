from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from admin.keyboards import *
from admin.support_reviews import keyboards, messages, branches, states
from admin.сallbacks import current_dispute, get_stars
from db.models import Supt, Reviews, User
from .keyboards import *

class Nums:
    num_review = 0
    num_pass = 0


async def start_review_menu(call: types.CallbackQuery, state: FSMContext):
    Nums.num_pass = 0
    await call.bot.edit_message_reply_markup(reply_markup=keyboards.support_review_keyboard,
                                             message_id=call.message.message_id,
                                             chat_id=call.message.chat.id)
    await call.answer()


async def back(call: types.CallbackQuery, state: FSMContext):
    await call.bot.edit_message_reply_markup(reply_markup=support_menu_keyboard,
                                             message_id=call.message.message_id,
                                             chat_id=call.message.chat.id)
    await call.answer()


async def back_to_review(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_message(call.message.chat.id,
                                text="💚 Поддержка и отзывы", reply_markup=keyboards.support_review_keyboard)
    await call.answer()


async def start_review(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    await call.message.answer(text=messages.start_review_msg,
                              reply_markup=keyboards.new_review_keyboard)
    await call.answer()


async def start_pass_review(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    await call.message.answer(text=messages.start_pass_msg,
                              reply_markup=keyboards.new_review_pass_keyboard)
    await call.answer()


async def get_review(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    Nums.num_review += 1
    await branches.write_quest(Nums.num_review, message=call.message)
    await call.answer()


async def get_pass_review(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    await branches.write_pass_quest(Nums.num_review, Nums.num_pass, message=call.message)
    await call.answer()


async def review_sup(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="Введи ответ пользователю:")
    await states.ReviewStates.input_review.set()
    await call.answer()


async def review_pass_sup(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="Введи ответ пользователю:")
    await states.ReviewStates.input_pass_review.set()
    await call.answer()


async def pass_sup(call: types.CallbackQuery, state: FSMContext):
    sup = await Supt.objects.filter(solved="new").afirst()
    sup.solved = "in_process"
    sup.save()
    await get_review(call, state)
    await call.answer()


async def pass_pass_sup(call: types.CallbackQuery, state: FSMContext):
    Nums.num_pass += 1
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    await branches.write_pass_quest(Nums.num_review, Nums.num_pass, message=call.message)
    await call.answer()


async def archive(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=messages.archive_msg, reply_markup=keyboards.archive_keyboard)
    await states.ReviewStates.archive.set()
    await call.answer()


async def archive_back(call: types.CallbackQuery, state: FSMContext):
    await states.ReviewStates.none.set()
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_message(call.message.chat.id,
                                text="💚 Поддержка и отзывы", reply_markup=keyboards.support_review_keyboard)
    await call.answer()


async def feedback(call: types.CallbackQuery, state: FSMContext):
    await call.bot.edit_message_reply_markup(reply_markup=keyboards.feedback_keyboard,
                                             message_id=call.message.message_id,
                                             chat_id=call.message.chat.id)
    await call.answer()


async def f(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)

    new_review = await Reviews.objects.filter(state_t="new").afirst()

    if new_review is None:
        await call.message.answer(text="нет отзывов")
    else:
        user = await User.objects.filter(user_id=new_review.user_id).alast()
        id_dispute = new_review.id_dispute
        action = current_dispute(user.action, user.additional_action)
        mark = get_stars(new_review.mark)

        tmp_msg = (f"Новый отзыв\n"
                   f"🧊Диспут #D{id_dispute}\n"
                   f"Имя: {new_review.user_name}\n"
                   f"Город: {new_review.city}\n"
                   f"Цель: {action}\n"
                   f"В игре: {30 - user.count_days}\n"
                   f"Оценка: {mark}\n"
                   f"Отзыв: {new_review.coment}\n")

        await state.update_data(user_id=new_review.user_id, id_dispute=new_review.id_dispute, chat_id=new_review.chat_id)
        await call.message.answer(text=tmp_msg, reply_markup=publish_or_not_keyboard)


    await call.answer()

async def bad_review(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    refuse = await Reviews.objects.filter(user_id=data['user_id'], id_dispute=data['id_dispute']).alast()
    refuse.state_t = Reviews.StateReview.bad_review
    refuse.save()

    await call.message.answer(text="Введи ответ пользователю:")


def register_callback(dp: Dispatcher, bot):
    dp.register_callback_query_handler(start_review_menu, text='supp',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(back, text='back_sup',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(start_review, text='new_review',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(start_pass_review, text='delayed',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(back_to_review, text='back_to_reviews',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(get_review, text='start_review',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(review_sup, text='review_sup',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(review_pass_sup, text='review_pass_sup',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(pass_sup, text='pass_sup',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(pass_pass_sup, text='pass_pass_sup',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(get_pass_review, text='start_pass_review',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(archive, text='archive_rev',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(archive_back, text='archive_back',
                                       state=states.ReviewStates.archive)
    dp.register_callback_query_handler(archive_back, text='archive_back',
                                       state=states.ReviewStates.archive)
    dp.register_callback_query_handler(feedback, text='feedback',
                                       state="*")
    dp.register_callback_query_handler(f, text='new_feedback',
                                       state="*")
    dp.register_callback_query_handler(f, text='not_public',
                                       state="*")
