from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from client.branches.start.messages import *
from client.branches.start.keyboards import *


async def second_message(call: types.CallbackQuery):
    await call.message.edit_text(text=second_faq_msg, reply_markup=second_buttons)
    await call.answer()


async def previous_first_message(call: types.CallbackQuery):
    await call.message.edit_text(text=first_faq_msg, reply_markup=first_button)
    await call.answer()


async def third_message(call: types.CallbackQuery):
    await call.message.edit_text(text=third_faq_msg, reply_markup=third_buttons)
    await call.answer()


async def previous_second_message(call: types.CallbackQuery):
    await call.message.edit_text(text=second_faq_msg, reply_markup=second_buttons)
    await call.answer()


async def fourth_message(call: types.CallbackQuery):
    await call.message.edit_text(text=fourth_faq_msg, reply_markup=fourth_button)
    await call.answer()


async def previous_third_message(call: types.CallbackQuery):
    await call.message.edit_text(text=third_faq_msg, reply_markup=third_buttons)
    await call.answer()


async def delete_message(call: types.CallbackQuery):

    await call.message.delete()
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(second_message, text='next_two', state="*")
    dp.register_callback_query_handler(previous_first_message, text='return_first', state="*")

    dp.register_callback_query_handler(previous_second_message, text='return_second', state="*")
    dp.register_callback_query_handler(third_message, text='next_three', state="*")

    dp.register_callback_query_handler(fourth_message, text='next_four', state="*")
    dp.register_callback_query_handler(previous_third_message, text='return_three', state="*")

    dp.register_callback_query_handler(delete_message, text="confirm", state="*")
