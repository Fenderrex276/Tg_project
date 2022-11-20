from aiogram import types

admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.add(types.KeyboardButton("✅ Репорты"), types.KeyboardButton("💚 Поддержка и отзывы"))

reports_menu_keyboard = types.InlineKeyboardMarkup()
reports_menu_keyboard.add(types.InlineKeyboardButton(text="Ежедневные", callback_data="every_day"))
reports_menu_keyboard.add(types.InlineKeyboardButton(text="Тестовые", callback_data="test_videos"))
reports_menu_keyboard.add(types.InlineKeyboardButton(text="До результата", callback_data="before_result"))
reports_menu_keyboard.add(types.InlineKeyboardButton(text="Архив", callback_data="archive"))

test_keyboard = types.InlineKeyboardMarkup()
test_keyboard.add(types.InlineKeyboardButton(text="⛔️ Не ок", callback_data="bad"),
                  types.InlineKeyboardButton(text="👍 Ок", callback_data="good"))
# test_keyboard.add(types.InlineKeyboardButton(text="Не видно лица / Результатов", callback_data="face_result"))
# test_keyboard.add(types.InlineKeyboardButton(text="Неверный код / Не слышно кода", callback_data="incorrect_code"))
# test_keyboard.add(types.InlineKeyboardButton(text="Ввести сообщение", callback_data="send_message"))

access_keyboard = types.InlineKeyboardMarkup(row_width=2)
access_keyboard.add(types.InlineKeyboardButton(text='👍 Верно', callback_data='confirm_video'),
                    types.InlineKeyboardButton(text='Назад', callback_data='back_to_video'))

refused_keyboard = types.InlineKeyboardMarkup()
refused_keyboard.add(types.InlineKeyboardButton(text="Не видно лица / Результатов", callback_data="face_result"))
refused_keyboard.add(types.InlineKeyboardButton(text="Неверный код / Не слышно кода", callback_data="incorrect_code"))
refused_keyboard.add(types.InlineKeyboardButton(text="Ввести сообщение", callback_data="send_message"))

support_menu_keyboard = types.InlineKeyboardMarkup()
support_menu_keyboard.add(types.InlineKeyboardButton(text="Поддержка", callback_data="supp"))
support_menu_keyboard.add(types.InlineKeyboardButton(text="Отзывы", callback_data="feedback"))
support_menu_keyboard.add(types.InlineKeyboardButton(text="⚡️ Системные сообщения", callback_data="sys_msg"))
support_menu_keyboard.add(types.InlineKeyboardButton(text="⭐️ DisputeAward", callback_data="dispute_award"))

