import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from aiogram.utils.markdown import link

from client.branches.knowledge_base.films import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute

# films

UserFilms = {}
def getFilm(call: types.CallbackQuery): #POS = Principle of success
    try:
        film_number = UserFilms[call.message.chat.id]
        UserFilms[call.message.chat.id] += 1
        if film_number == len(messages.films):
            UserFilms[call.message.chat.id] = 0
    except:
        UserFilms[call.message.chat.id] = 0
        film_number = 0
    return film_number

async def choose_fm(call: types.CallbackQuery):
    await call.message.edit_text(text=messages.films_msg, reply_markup=keyboards.start_fm_keyboard,
                                 parse_mode=ParseMode.MARKDOWN)
    await call.answer()

async def read_fm(call: types.CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)

    fn = getFilm(call)
    l = link(title='Трейлер:', url=messages.trailers[fn])

    await call.message.answer(text=f"{messages.films[fn]}{l}", reply_markup=keyboards.control_fm_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()

async def dislike_fm(call: types.CallbackQuery):
    try:
        fn = getFilm(call)

        l = link(title='Трейлер:', url=messages.trailers[fn])
        await call.message.answer(text=f"{messages.films[fn]}{l}", reply_markup=keyboards.control_fm_keyboard,
                                  parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await dislike_fm(call)


async def like_fm(call: types.CallbackQuery):
    fn = getFilm(call)
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
    #await call.bot.send_video(call.message.chat.id, 'https://youtu.be/1JbcDpNh7hM')
    l = link(title='Трейлер:', url=messages.trailers[fn])

    await call.message.answer(text=f"{messages.films[fn]}{l}", reply_markup=keyboards.control_fm_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()

def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_fm, text='mediateka',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_fm, text='start_fm',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(like_fm, text='like_fm',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_fm, text='dislike_fm',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(read_fm, text='films',
                                       state=StatesDispute.knowledge_base)
