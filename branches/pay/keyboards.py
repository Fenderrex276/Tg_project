from aiogram import types


choose_sum_keyboard = types.InlineKeyboardMarkup()
choose_sum_keyboard.add(types.InlineKeyboardButton(text='15 000 ₽', callback_data='15 000'))
choose_sum_keyboard.add(types.InlineKeyboardButton(text='30 000 ₽', callback_data='30 000'))
choose_sum_keyboard.add(types.InlineKeyboardButton(text='50 000 ₽', callback_data='50 000'))
choose_sum_keyboard.add(types.InlineKeyboardButton(text='100 000 ₽', callback_data='100 000'))
choose_sum_keyboard.add(types.InlineKeyboardButton(text='Другая сумма', callback_data='other_sum'))

get_banking_detials_keyboard = types.InlineKeyboardMarkup()
get_banking_detials_keyboard.add(types.InlineKeyboardButton(text='👍 Получить реквизиты', callback_data='get_details'))
get_banking_detials_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_choose_sum'))

confirm_deposit_payed_keyboard = types.InlineKeyboardMarkup()
confirm_deposit_payed_keyboard.add(types.InlineKeyboardButton(text='Подтвердить', callback_data='access'),
                                   types.InlineKeyboardButton(text='Отменить', callback_data='cancel_pay'))

go_keyboard = types.InlineKeyboardMarkup()
go_keyboard.add(types.InlineKeyboardButton(text='Вперёд ✊', callback_data='go_disput'))

next_step_keyboard = types.InlineKeyboardMarkup()
next_step_keyboard.add(types.InlineKeyboardButton(text='🎓 Начать (≈3 мин.)', callback_data='step_to_test_video_note'))
