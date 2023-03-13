import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.principles_of_success import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute


# principle_of_success

UserPos = {}
def getPOS(call: types.CallbackQuery): #POS = Principle of success
    try:
        pos_number = UserPos[call.message.chat.id]
        UserPos[call.message.chat.id] += 1
        if pos_number == len(messages.tips):
            UserPos[call.message.chat.id] = 0
    except:
        UserPos[call.message.chat.id] = 0
        pos_number = 0
    return pos_number


async def choose_ps(call: types.CallbackQuery):
    await call.message.edit_text(text=messages.principles_of_success_msg, reply_markup=keyboards.start_ps_keyboard,
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def read_ps(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    tip = getPOS(call)
    await call.message.answer(text=messages.tips[tip], reply_markup=keyboards.control_ps_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def dislike_ps(call: types.CallbackQuery):
    try:
        tip = getPOS(call)
        await call.message.edit_text(text=messages.tips[tip], reply_markup=keyboards.control_ps_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await dislike_ps(call)


async def like_ps(call: types.CallbackQuery):
    tip = getPOS(call)
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.message.answer(text=messages.tips[tip], reply_markup=keyboards.control_ps_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_ps, text='principle_of_success',
                                       state="*")
    dp.register_callback_query_handler(dislike_ps, text='start_ps',
                                       state="*")
    dp.register_callback_query_handler(like_ps, text='like_ps',
                                       state="*")
    dp.register_callback_query_handler(dislike_ps, text='dislike_ps',
                                       state="*")
    dp.register_callback_query_handler(read_ps, text='read_ps',
                                       state="*")
