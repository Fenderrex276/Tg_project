from aiogram import types

start_md_keyboard = types.InlineKeyboardMarkup(row_width=1)
start_md_keyboard.add(types.InlineKeyboardButton(text='👍 Читать', callback_data='read_faq'))
start_md_keyboard.add(types.InlineKeyboardButton(text='❓ Задать свой вопрос', callback_data='my_quest'))


control_md_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_md_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='next_faq'),
                        types.InlineKeyboardButton(text='Назад', callback_data="back_faq"))
