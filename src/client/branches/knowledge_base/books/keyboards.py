from aiogram import types

control_bk_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_bk_keyboard.add(types.InlineKeyboardButton(text='🎥 Фильмы', callback_data='films'),
                        types.InlineKeyboardButton(text='📣 Поделиться', switch_inline_query="Telegram"))
control_bk_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_bk'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_bk'))
