import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from client.branches.knowledge_base.memes import messages, states, keyboards
from client.branches.thirty_days_dispute.states import StatesDispute

# memes

async def dislike_meme(call: types.CallbackQuery):
    try:
        rand = random.randrange(136)+1
        photo = InputFile(f"client/media/memes/0{rand}.jpg")
        await call.bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=keyboards.control_memes_keyboard,
                                  caption="")
        await call.answer()
    except:
        await dislike_meme(call)


async def like_meme(call: types.CallbackQuery):
    rand = random.randrange(136) + 1
    photo = InputFile(f"client/media/memes/0{rand}.jpg")
    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id)
    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=keyboards.control_memes_keyboard,
                              caption="")
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(dislike_meme, text='memes',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(like_meme, text='like_meme',
                                       state=StatesDispute.knowledge_base)
    dp.register_callback_query_handler(dislike_meme, text='dislike_meme',
                                       state=StatesDispute.knowledge_base)
