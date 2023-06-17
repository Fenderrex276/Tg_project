from aiogram import types

administration_menu_keyboard = types.InlineKeyboardMarkup()
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Администраторы", callback_data="admins"))
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Промокоды", callback_data="promo_codes"))
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Оповещение пользователей", callback_data="notification_users"))
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Оповещение администраторов", callback_data="notification_admins"))
administration_menu_keyboard.add(types.InlineKeyboardButton(text="Статистика", callback_data="statistic"))
