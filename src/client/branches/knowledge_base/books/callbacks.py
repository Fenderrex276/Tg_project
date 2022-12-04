import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.books import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute


# books

async def books(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    rand = random.randrange(len(messages.books))

    await call.message.answer(text=messages.books[rand], reply_markup=keyboards.control_bk_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def dislike_bk(call: types.CallbackQuery):
    try:
        await call.bot.delete_message(call.message.chat.id, call.message.message_id)
        rand = random.randrange(len(messages.books))
        await call.message.answer(text=messages.books[rand], reply_markup=keyboards.control_bk_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await dislike_bk(call)


async def like_bk(call: types.CallbackQuery):
    rand = random.randrange(len(messages.books))
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.message.answer(text=messages.books[rand], reply_markup=keyboards.control_bk_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(books, text='kb_books',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(like_bk, text='like_bk',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_bk, text='dislike_bk',
                                       state=StatesDispute.knowledge_base)
