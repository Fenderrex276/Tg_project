from aiogram import types

supdis_keyboard = types.InlineKeyboardMarkup(row_width=2)
supdis_keyboard.add(types.InlineKeyboardButton(text='🔴 Смотреть', callback_data='ted'),
                    types.InlineKeyboardButton(text='📰 Читать', callback_data='md'))
supdis_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_supdis'),
                    types.InlineKeyboardButton(text='👎', callback_data='dislike_supdis'))
