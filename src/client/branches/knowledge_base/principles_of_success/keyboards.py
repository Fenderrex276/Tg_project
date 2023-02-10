from aiogram import types

start_ps_keyboard = types.InlineKeyboardMarkup(row_width=2)
start_ps_keyboard.add(types.InlineKeyboardButton(text='👍 Начнём', callback_data='start_ps'))


control_ps_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_ps_keyboard.add(types.InlineKeyboardButton(text='👾 Мемы', callback_data='memes'))
control_ps_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_ps'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_ps'))
