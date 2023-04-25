

import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.supdis import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute

UserSubdis = {}


def getSubdis(call: types.CallbackQuery):
    try:
        UserSubdis[call.message.chat.id] += 1
        ted_number = UserSubdis[call.message.chat.id]
        if ted_number == 550:
            UserSubdis[call.message.chat.id] = 120
            ted_number = UserSubdis[call.message.chat.id]
    except:
        UserSubdis[call.message.chat.id] = random.randint(530, 550)
        ted_number = UserSubdis[call.message.chat.id]
    return ted_number


async def dislike_supdis(call: types.CallbackQuery):
    sd = getSubdis(call)
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_audio(call.message.chat.id, messages.supdis_link + str(sd),
                              reply_markup=keyboards.supdis_keyboard)
    await call.answer()


async def like_supdis(call: types.CallbackQuery):
    sd = getSubdis(call)
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.bot.send_audio(call.message.chat.id, messages.supdis_link + str(sd),
                              reply_markup=keyboards.supdis_keyboard)
    await call.answer()


async def supdis(call: types.CallbackQuery):
    sd = getSubdis(call)
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_audio(call.message.chat.id, messages.supdis_link+str(sd),
                              reply_markup=keyboards.supdis_keyboard)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(supdis, text='supdis',
                                       state="*")
    dp.register_callback_query_handler(like_supdis, text='like_supdis',
                                       state="*")
    dp.register_callback_query_handler(dislike_supdis, text='dislike_supdis',
                                       state="*")
