from aiogram import types

test_confirm_keyboard = types.InlineKeyboardMarkup()
test_confirm_keyboard.add(types.InlineKeyboardButton(text='😌 Испытать', callback_data='next_one'))

send_video_keyboard = types.InlineKeyboardMarkup(row_width=2)
send_video_keyboard.add(types.InlineKeyboardButton(text='🚀 Отправить', callback_data='send_video'),
                          types.InlineKeyboardButton(text='Новое видео', callback_data='send_new_video'))
