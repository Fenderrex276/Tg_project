from aiogram import types

start_md_keyboard = types.InlineKeyboardMarkup(row_width=1)
start_md_keyboard.add(types.InlineKeyboardButton(text='Открыть  🏳️', callback_data='start_md'))


control_md_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_md_keyboard.add(types.InlineKeyboardButton(text='🔊 Слушать', switch_inline_query="supdis"),
                        types.InlineKeyboardButton(text='🔴 Смотреть', callback_data='ted'))
control_md_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_md'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_md'))
