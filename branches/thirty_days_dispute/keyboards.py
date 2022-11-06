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
knowledge_base_keyboard.add(types.InlineKeyboardButton(text='👍🏼 Отзывы об игре', callback_data='reviews'))


account_keyboard = types.InlineKeyboardMarkup(row_width=2)
account_keyboard.add(types.InlineKeyboardButton(text='💎 Моё имя', callback_data='change_name'),
                     types.InlineKeyboardButton(text='💰 Депозит', callback_data='deposit'))
account_keyboard.add(types.InlineKeyboardButton(text='🌍 Часовой пояс', callback_data='timezone'),
                     types.InlineKeyboardButton(text='🆘 Поддержка', callback_data='support'))


change_name_keyboard = types.InlineKeyboardMarkup(row_width=2)
change_name_keyboard.add(types.InlineKeyboardButton(text='Изменить', callback_data="change_name_access"),
                         types.InlineKeyboardButton(text='Оставить так', callback_data="cancel_change_name"))

