import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.books import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute


# books
UserBooks = {}

def getBook(call: types.CallbackQuery):
    try:
        book_number = UserBooks[call.message.chat.id]
        UserBooks[call.message.chat.id] += 1
        if book_number == len(messages.books):
            UserBooks[call.message.chat.id] = 0
    except:
        UserBooks[call.message.chat.id] = 0
        book_number = 0
    return book_number

async def books(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    bn = getBook(call)
    await call.message.answer(text=messages.books[bn], reply_markup=keyboards.control_bk_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
    await call.answer()


async def dislike_bk(call: types.CallbackQuery):
    try:
        await call.bot.delete_message(call.message.chat.id, call.message.message_id)
        bn = getBook(call)
        await call.message.answer(text=messages.books[bn], reply_markup=keyboards.control_bk_keyboard,
                                     parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await dislike_bk(call)


async def like_bk(call: types.CallbackQuery):
    bn = getBook(call)
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.message.answer(text=messages.books[bn], reply_markup=keyboards.control_bk_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(books, text='kb_books',
                                       state="*")
    dp.register_callback_query_handler(like_bk, text='like_bk',
                                       state="*")
    dp.register_callback_query_handler(dislike_bk, text='dislike_bk',
                                       state="*")
