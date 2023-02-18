from aiogram import types


def createKeyboard(buttons: list, rows: list = None) -> types.ReplyKeyboardMarkup:
    if rows is None:
        rows = [1] * len(buttons)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_buttons = [types.KeyboardButton(x) for x in buttons]

    index = 0
    for amount in rows:
        keyboard.row(*new_buttons[index: index + amount])
        index += amount

    return keyboard


buttons_menu = ["✅ Путь героя", "💚 База знаний", "🟢 Аккаунт"]
menu_keyboard = createKeyboard(buttons_menu, [1, 2])

report_diary_keyboard = types.InlineKeyboardMarkup()
report_diary_keyboard.add(types.InlineKeyboardButton(text='🗣 Репорт', callback_data='report'))
report_diary_keyboard.add(types.InlineKeyboardButton(text='📝 Дневник', callback_data='diary'))

report_keyboard = types.InlineKeyboardMarkup(row_width=2)
report_keyboard.add(types.InlineKeyboardButton(text='👑 Бонусы', callback_data='bonuses'),
                    types.InlineKeyboardButton(text='😇 Правила', callback_data='rules'))
report_keyboard.add(types.InlineKeyboardButton(text='Отправить репорт', callback_data='send_new_report'))

knowledge_base_keyboard = types.InlineKeyboardMarkup()
knowledge_base_keyboard.add(types.InlineKeyboardButton(text='🍎 Принципы успеха', callback_data='principle_of_success'))
knowledge_base_keyboard.add(types.InlineKeyboardButton(text='🎪 Медиатека', callback_data='mediateka'))
knowledge_base_keyboard.add(types.InlineKeyboardButton(text='🥺 Минута отчаяния', callback_data='despair'))
knowledge_base_keyboard.add(types.InlineKeyboardButton(text='🧠 FAQ', callback_data='faq'))
knowledge_base_keyboard.add(types.InlineKeyboardButton(text='👍🏼 Отзывы об игре', url='https://t.me/DisputeGame'))


account_keyboard = types.InlineKeyboardMarkup(row_width=2)
account_keyboard.add(types.InlineKeyboardButton(text='💎 Моё имя', callback_data='change_name'),
                     types.InlineKeyboardButton(text='💰 Депозит', callback_data='deposit'))
account_keyboard.add(types.InlineKeyboardButton(text='🌍 Часовой пояс', callback_data='change_timezone'),
                     types.InlineKeyboardButton(text='🆘 Поддержка', callback_data='support'))


change_name_keyboard = types.InlineKeyboardMarkup(row_width=2)
change_name_keyboard.add(types.InlineKeyboardButton(text='Изменить', callback_data="change_name_access"),
                         types.InlineKeyboardButton(text='Оставить так', callback_data="cancel_change_name"))


admit_or_pass_keyboard = types.InlineKeyboardMarkup(row_width=2)
admit_or_pass_keyboard.add(types.InlineKeyboardButton(text='Признаться', callback_data='admit'),
                           types.InlineKeyboardButton(text='Пасс', callback_data='pass'))


awards_keyboard = types.InlineKeyboardMarkup(row_width=2)
awards_keyboard.add(types.InlineKeyboardButton(text='🎟 Промо-код', callback_data='1promo_code1'),
                    types.InlineKeyboardButton(text='⭐️ DisputeAward', callback_data='dispute_award'))
awards_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='return_to_reports'))


send_video_keyboard = types.InlineKeyboardMarkup(row_width=2)
send_video_keyboard.add(types.InlineKeyboardButton(text='🚀 Отправить', callback_data='send_video'),
                        types.InlineKeyboardButton(text='Новое видео', callback_data='send_new_video'))


end_game_keyboard = types.InlineKeyboardMarkup(row_width=2)
end_game_keyboard.add(types.InlineKeyboardButton(text='Оставить ✌️ отзыв', callback_data='new_review'),
                      types.InlineKeyboardButton(text='Спорим 🤝 ещё', callback_data='new_dispute'))

buttons_menu1 = ["🤜 Спорим 🤛", "💚 База знаний", "🟢 Аккаунт"]
new_menu_keyboard = createKeyboard(buttons_menu1, [1, 2])



mark_keyboard = types.InlineKeyboardMarkup()
mark_keyboard.add(types.InlineKeyboardButton(text="️⭐️", callback_data="one"))
mark_keyboard.add(types.InlineKeyboardButton(text="⭐️⭐️", callback_data="two"))
mark_keyboard.add(types.InlineKeyboardButton(text="️⭐️⭐️⭐️", callback_data="three"))
mark_keyboard.add(types.InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data="four"))
mark_keyboard.add(types.InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️", callback_data="five"))