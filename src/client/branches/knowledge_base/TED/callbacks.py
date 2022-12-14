# https://t.me/c/1752556958/253


import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.TED import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute


async def dislike_ted(call: types.CallbackQuery):
    rand = random.randrange(len(messages.teds))
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_video(call.message.chat.id, messages.teds[rand],
                              reply_markup=keyboards.control_ted_keyboard)
    await call.answer()
#TODO сделать словарь где название теда ключ, значение - сам видос

async def like_ted(call: types.CallbackQuery):
    rand = random.randrange(len(messages.teds))
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.bot.send_video(call.message.chat.id, messages.teds[rand],
                              reply_markup=keyboards.control_ted_keyboard)
    await call.answer()


async def ted(call: types.CallbackQuery):
    rand = random.randrange(len(messages.teds))
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.send_video(call.message.chat.id, messages.teds[rand],
                              reply_markup=keyboards.control_ted_keyboard)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(ted, text='ted',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(like_ted, text='like_ted',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_ted, text='dislike_ted',
                                       state=StatesDispute.knowledge_base)
