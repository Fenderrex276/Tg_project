from aiogram import types

start_md_keyboard = types.InlineKeyboardMarkup(row_width=1)
start_md_keyboard.add(types.InlineKeyboardButton(text='Открыть', callback_data='start_md'))


control_md_keyboard = types.InlineKeyboardMarkup(row_width=2)
control_md_keyboard.add(types.InlineKeyboardButton(text='🔴 TED', callback_data='ted'),
                        types.InlineKeyboardButton(text='📣 Поделиться', switch_inline_query="Telegram"))
control_md_keyboard.add(types.InlineKeyboardButton(text='👍', callback_data='like_md'),
                        types.InlineKeyboardButton(text='👎', callback_data='dislike_md'))
