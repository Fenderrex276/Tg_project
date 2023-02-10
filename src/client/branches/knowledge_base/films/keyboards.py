from aiogram import types

start_fm_keyboard = types.InlineKeyboardMarkup(row_width=1)
start_fm_keyboard.add(types.InlineKeyboardButton(text='Вдохновиться 🔥', callback_data='start_fm'))


control_fm_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_fm_keyboard.add(types.InlineKeyboardButton(text='📗 Книги', callback_data='kb_books'))
control_fm_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_fm'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_fm'))
