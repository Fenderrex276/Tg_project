from aiogram import Dispatcher, types
from aiogram.types import InputFile, ParseMode, InputMedia
from branches.knowledge_base.FAQ import messages, states, keyboards, branches


async def next_faq(call: types.CallbackQuery):
    try:
        branches.faqs[call.message.chat.id] += 1
        i = branches.faqs[call.message.chat.id]
        await call.message.answer(text=messages.quests[i], reply_markup=keyboards.control_md_keyboard,
                                  parse_mode=ParseMode.MARKDOWN)
        await call.answer()
    except:
        await first_faq(call)


async def prev_faq(call: types.CallbackQuery):
    try:
        i = branches.faqs[call.message.chat.id]
        if i == 0:
            await choose_faq(call)
        else:
            branches.faqs[call.message.chat.id] -= 1
            i = branches.faqs[call.message.chat.id]
            await call.message.answer(text=messages.quests[i], reply_markup=keyboards.control_md_keyboard,
                                  parse_mode=ParseMode.MARKDOWN)
            await call.answer()
    except:
        await first_faq(call)


async def first_faq(call: types.CallbackQuery):
    await call.message.edit_text(text=messages.quests[0], reply_markup=keyboards.control_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    branches.faqs[call.message.chat.id] = 0
    await call.answer()


async def choose_faq(call: types.CallbackQuery):
    await call.bot.delete_message(message_id=call.message.message_id,chat_id= call.message.chat.id)
    await call.message.answer(text=messages.start_FAQ, reply_markup=keyboards.start_md_keyboard,
                              parse_mode=ParseMode.MARKDOWN)
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(choose_faq, text='faq',
                                       state="*")
    dp.register_callback_query_handler(first_faq, text='read_faq',
                                       state="*")
    dp.register_callback_query_handler(next_faq, text='next_faq',
                                       state="*")
    dp.register_callback_query_handler(prev_faq, text='back_faq',
                                       state="*")
