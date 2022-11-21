from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from admin.support_reviews import keyboards, messages, branches, states
from admin.states import AdminStates
from admin.keyboards import support_menu_keyboard


num_review = 0


async def start_review_menu(call: types.CallbackQuery, state: FSMContext):
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


async def get_review(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    await branches.write_quest(num_review, message=call.message)
    await call.answer()

async def review_sup(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="Введи ответ пользователю:")
    await state.get_data()
    await call.answer()

def register_callback(dp: Dispatcher, bot):
    dp.register_callback_query_handler(start_review_menu, text='supp',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(back, text='back_sup',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(start_review, text='new_review',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(back_to_review, text='back_to_reviews',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(get_review, text='start_review',
                                       state=states.ReviewStates.none)
    dp.register_callback_query_handler(review_sup, text='review_sup',
                                       state=states.ReviewStates.none)