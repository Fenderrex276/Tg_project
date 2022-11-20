from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_review_keyboard = InlineKeyboardMarkup()
support_review_keyboard.add(InlineKeyboardButton(text="Новые вопросы", callback_data="new_review"))
support_review_keyboard.add(InlineKeyboardButton(text="Вопросы оплаты", callback_data="payment_review"))
support_review_keyboard.add(InlineKeyboardButton(text="Отложенные", callback_data="delayed"))
support_review_keyboard.add(InlineKeyboardButton(text="Архив", callback_data="archive"))
support_review_keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_sup"))

new_review_keyboard = InlineKeyboardMarkup(row_width=2)
new_review_keyboard.add(InlineKeyboardButton(text='🔥 Начать', callback_data='start_review'),
                        InlineKeyboardButton(text='Назад', callback_data='back_to_reviews'))

review_keyboard = InlineKeyboardMarkup(row_width=2)
review_keyboard.add(InlineKeyboardButton(text='Ответить', callback_data='review_sup'),
                        InlineKeyboardButton(text='Пасс', callback_data='pass_sup'))
