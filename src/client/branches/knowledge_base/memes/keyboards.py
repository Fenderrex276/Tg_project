from aiogram import types

control_memes_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_memes_keyboard.add(types.InlineKeyboardButton(text='🎓 Читать', callback_data='read_ps'))
control_memes_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_meme'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_meme'))