from aiogram import types

administration_menu_keyboard = types.InlineKeyboardMarkup()
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Администраторы", callback_data="admins"))
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Промокоды", callback_data="promo_codes"))
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Оповещение", callback_data="notification"))

actions_with_admins = types.InlineKeyboardMarkup()
actions_with_admins.add(types.InlineKeyboardButton(text="К диалогу", callback_data="dialogs_with_admin"))
actions_with_admins.add(types.InlineKeyboardButton(text="Удалить", callback_data="delete_admin"))
