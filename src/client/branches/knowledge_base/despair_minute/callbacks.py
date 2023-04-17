import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode, InputMedia
from client.branches.knowledge_base.despair_minute import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute

# despair minute

UserTips = {}


def getTips(call: types.CallbackQuery):
    try:
        pos_number = UserTips[call.message.chat.id]
        UserTips[call.message.chat.id] += 1
        if pos_number == len(messages.tips):
            UserTips[call.message.chat.id] = 0
    except:
        UserTips[call.message.chat.id] = random.randint(0, len(messages.tips)-1)
        pos_number = UserTips[call.message.chat.id]
    return pos_number


async def choose_ps(call: types.CallbackQuery):
    photo = InputFile("client/media/kb_md/start_mb.jpg")
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text=messages.start_msg, reply_markup=keyboards.start_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def md(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    tip = getTips(call)
    await call.message.answer(text=messages.tips[tip], reply_markup=keyboards.control_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def dislike_ps(call: types.CallbackQuery):
    try:
        pos = getTips(call)
        await call.message.edit_text(text=messages.tips[pos], reply_markup=keyboards.control_md_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await dislike_ps(call)


async def like_ps(call: types.CallbackQuery):
    pos = getTips(call)
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.message.answer(text=messages.tips[pos], reply_markup=keyboards.control_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_ps, text='despair',
                                       state="*")
    dp.register_callback_query_handler(dislike_ps, text='start_md',
                                       state="*")
    dp.register_callback_query_handler(like_ps, text='like_md',
                                       state="*")
    dp.register_callback_query_handler(dislike_ps, text='dislike_md',
                                       state="*")
    dp.register_callback_query_handler(md, text='md',
                                       state="*")
