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


buttons_menu = ["🤜 Спорим 🤛", "🫀FAQ", "👍Отзывы"]
menu_keyboard = createKeyboard(buttons_menu, [1, 2])

next_two = types.InlineKeyboardButton(text='Дальше', callback_data='next_two')
first_button = types.InlineKeyboardMarkup().add(next_two)

second_buttons = types.InlineKeyboardMarkup(row_width=2)
return_one = types.InlineKeyboardButton(text='Назад', callback_data='return_first')
next_three = types.InlineKeyboardButton(text='Дальше', callback_data='next_three')
second_buttons.add(return_one, next_three)

third_buttons = types.InlineKeyboardMarkup(row_width=2)
return_two = types.InlineKeyboardButton(text='Назад', callback_data='return_second')
next_four = types.InlineKeyboardButton(text='Дальше', callback_data='next_four')
third_buttons.add(return_two, next_four)

fourth_button = types.InlineKeyboardMarkup(row_width=2)
previous = types.InlineKeyboardButton(text='Назад', callback_data='return_three')
i_confirm = types.InlineKeyboardButton(text='👍 Я понял', callback_data="confirm")
fourth_button.add(previous, i_confirm)
