import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.memes import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute

# memes

UserMemes = {}
def getMeme(call: types.CallbackQuery):
    try:
        meme_number = UserMemes[call.message.chat.id]
        UserMemes[call.message.chat.id] += 1
        if meme_number == 136:
            UserMemes[call.message.chat.id] = 1
    except:
        UserMemes[call.message.chat.id] = random.randint(1, 135)
        meme_number = UserMemes[call.message.chat.id]
    return meme_number

async def dislike_meme(call: types.CallbackQuery):
    try:
        meme = getMeme(call)
        photo = InputFile(f"client/media/memes/0{meme}.jpg")
        await call.bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=keyboards.control_memes_keyboard,
                                  caption="")
        await call.answer()
    except:
        await dislike_meme(call)


async def like_meme(call: types.CallbackQuery):
    meme = getMeme(call)
    photo = InputFile(f"client/media/memes/0{meme}.jpg")
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=keyboards.control_memes_keyboard,
                              caption="")
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(dislike_meme, text='memes',
                                       state="*")
    dp.register_callback_query_handler(like_meme, text='like_meme',
                                       state="*")
    dp.register_callback_query_handler(dislike_meme, text='dislike_meme',
                                       state="*")
