import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode, InputMedia
from branches.knowledge_base.despair_minute import messages, states, keyboards
from branches.thirty_days_dispute.states import StatesDispute

# principle_of_success

async def choose_ps(call: types.CallbackQuery):
    photo = InputFile("media/kb_md/start_mb.jpg")
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer_photo(photo=photo)
    await call.message.answer(text=messages.start_msg, reply_markup=keyboards.start_md_keyboard, parse_mode=ParseMode.MARKDOWN)
    await call.answer()

async def md(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    rand = random.randrange(len(messages.tips))
    await call.message.answer(text=messages.tips[rand], reply_markup=keyboards.control_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()

async def dislike_ps(call: types.CallbackQuery):
    try:
        rand = random.randrange(len(messages.tips))
        await call.message.edit_text(text=messages.tips[rand], reply_markup=keyboards.control_md_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await dislike_ps(call)


async def like_ps(call: types.CallbackQuery):
    rand = random.randrange(len(messages.tips))
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
    await call.message.answer(text=messages.tips[rand], reply_markup=keyboards.control_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()

def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_ps, text='despair',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_ps, text='start_md',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(like_ps, text='like_md',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_ps, text='dislike_md',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(md, text='md',
                                       state=StatesDispute.knowledge_base)
