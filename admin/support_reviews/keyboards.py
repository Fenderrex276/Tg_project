from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_review_keyboard = InlineKeyboardMarkup()
support_review_keyboard.add(InlineKeyboardButton(text="Новые вопросы", callback_data="supp"))
support_review_keyboard.add(InlineKeyboardButton(text="Вопросы оплаты", callback_data="feedback"))
support_review_keyboard.add(InlineKeyboardButton(text="Отложенные", callback_data="sys_msg"))
support_review_keyboard.add(InlineKeyboardButton(text="Архив", callback_data="dispute_award"))



