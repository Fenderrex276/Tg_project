from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_review_keyboard = InlineKeyboardMarkup()
support_review_keyboard.add(InlineKeyboardButton(text="Новые вопросы", callback_data="new_review"))
support_review_keyboard.add(InlineKeyboardButton(text="Вопросы оплаты", callback_data="payment_review"))
support_review_keyboard.add(InlineKeyboardButton(text="Отложенные", callback_data="delayed"))
support_review_keyboard.add(InlineKeyboardButton(text="Архив", callback_data="archive_rev"))
support_review_keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_sup"))

new_review_keyboard = InlineKeyboardMarkup(row_width=2)
new_review_keyboard.add(InlineKeyboardButton(text='🔥 Начать', callback_data='start_review'),
                        InlineKeyboardButton(text='Назад', callback_data='back_to_reviews'))

new_review_pass_keyboard = InlineKeyboardMarkup(row_width=2)
new_review_pass_keyboard.add(InlineKeyboardButton(text='🔥 Начать', callback_data='start_pass_review'),
                        InlineKeyboardButton(text='Назад', callback_data='back_to_reviews'))

review_keyboard = InlineKeyboardMarkup(row_width=2)
review_keyboard.add(InlineKeyboardButton(text='Ответить', callback_data='review_sup'),
                        InlineKeyboardButton(text='Пасс', callback_data='pass_sup'))

review_pass_keyboard = InlineKeyboardMarkup(row_width=2)
review_pass_keyboard.add(InlineKeyboardButton(text='Ответить', callback_data='review_pass_sup'),
                        InlineKeyboardButton(text='Пасс', callback_data='pass_pass_sup'))

archive_keyboard = InlineKeyboardMarkup(row_width=1)
archive_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='archive_back'))


feedback_keyboard = InlineKeyboardMarkup()
feedback_keyboard.add(InlineKeyboardButton(text="Новые отзывы", callback_data="new_feedback"))
feedback_keyboard.add(InlineKeyboardButton(text="Неопубликованные", callback_data="not_public"))
feedback_keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_sup"))


publish_or_not_keyboard = InlineKeyboardMarkup()
publish_or_not_keyboard.add(InlineKeyboardButton(text="Не принимать", callback_data="bad_review"))
publish_or_not_keyboard.add(InlineKeyboardButton(text="Опубликовать", callback_data="good_review"))
