from aiogram import types

control_ted_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_ted_keyboard.add(types.InlineKeyboardButton(text='📰 Читать', callback_data='md'),
                        types.InlineKeyboardButton(text='🔊 Слушать', switch_inline_query="supdis"))
control_ted_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_ted'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_ted'))

