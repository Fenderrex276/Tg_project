from aiogram import types


thirty_days_keyboard = types.InlineKeyboardMarkup()
thirty_days_keyboard.add(types.InlineKeyboardButton(text='Испытания воли (30 дней)', callback_data='thirty_days'))
thirty_days_keyboard.add(types.InlineKeyboardButton(text='Личные цели (90 дней)', callback_data='ninety_days'))

quit_back = types.InlineKeyboardButton(text='Ещё пример', callback_data='return_main')

test_selection_keyboard = types.InlineKeyboardMarkup()
test_selection_keyboard.add(types.InlineKeyboardButton(text='🚫 Брошу курить / пить / наркотики',
                                                       callback_data='quit_something'))
test_selection_keyboard.add(types.InlineKeyboardButton(text='🍔 Займусь спортом / похудею',
                                                       callback_data='sport_lose_weight'))
test_selection_keyboard.add(types.InlineKeyboardButton(text='🌤 Буду вставать рано утром',
                                                       callback_data='early_morning'))
test_selection_keyboard.add(types.InlineKeyboardButton(text='🇬🇧 Буду учить другой язык',
                                                       callback_data='other_language'))
test_selection_keyboard.add(types.InlineKeyboardButton(text='💰 Накоплю сумму денег', callback_data='more_money'))
test_selection_keyboard.add(types.InlineKeyboardButton(text='🎓 Научусь интересному', callback_data='study_new'))
test_selection_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_full_menu'))


drink_keyboard = types.InlineKeyboardMarkup()
drink_keyboard.add(types.InlineKeyboardButton(text='🍷 Брошу пить алкоголь', callback_data='quit_drink'))
drink_keyboard.add(types.InlineKeyboardButton(text='🚬 Брошу курить никотин', callback_data='quit_smoking'))
drink_keyboard.add(types.InlineKeyboardButton(text='💊 Брошу употреблять наркотики', callback_data='quit_drugs'))
drink_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_quit_menu'))


lose_weight_keyboard = types.InlineKeyboardMarkup()
lose_weight_keyboard.add(types.InlineKeyboardButton(text='💪 Буду ходить в зал', callback_data='gym'))
lose_weight_keyboard.add(types.InlineKeyboardButton(text='🌱 Похудею на 5 кг', callback_data='lose_weight'))
lose_weight_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_quit_menu'))


teach_something_keyboard = types.InlineKeyboardMarkup()
teach_something_keyboard.add(types.InlineKeyboardButton(text='🍏 Научусь готовить здоровую еду',
                                                        callback_data='healthy_food'))
teach_something_keyboard.add(types.InlineKeyboardButton(text='💻 Научусь программировать', callback_data='programming'))
teach_something_keyboard.add(types.InlineKeyboardButton(text='🎼 Научусь играть на...', callback_data='learn_play'))
teach_something_keyboard.add(types.InlineKeyboardButton(text='🎨 Научусь рисовать', callback_data='painting'))
teach_something_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_quit_menu'))

confirm_alcohol_keyboard = types.InlineKeyboardMarkup()
confirm_alcohol_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_quit_alcohol'))
confirm_alcohol_keyboard.add(types.InlineKeyboardButton(text='Ещё пример', callback_data='return_main'))

confirm_smoking_keyboard = types.InlineKeyboardMarkup()
confirm_smoking_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_quit_smoking'))
confirm_smoking_keyboard.add(types.InlineKeyboardButton(text='Ещё пример', callback_data='return_main'))

confirm_drugs_keyboard = types.InlineKeyboardMarkup()
confirm_drugs_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_quit_drugs'))
confirm_drugs_keyboard.add(types.InlineKeyboardButton(text='Ещё пример', callback_data='return_main'))

confirm_gym_keyboard = types.InlineKeyboardMarkup()
confirm_gym_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_go_gym'))
confirm_gym_keyboard.add(quit_back)

confirm_lose_weight_keyboard = types.InlineKeyboardMarkup()
confirm_lose_weight_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_lose_weight'))
confirm_lose_weight_keyboard.add(quit_back)

confirm_early_morning_keyboard = types.InlineKeyboardMarkup()
confirm_early_morning_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_early_morning'))
confirm_early_morning_keyboard.add(quit_back)

confirm_other_language = types.InlineKeyboardMarkup()
confirm_other_language.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_other_language'))
confirm_other_language.add(quit_back)

confirm_more_money_keyboard = types.InlineKeyboardMarkup()
confirm_more_money_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_more_money'))
confirm_more_money_keyboard.add(quit_back)

confirm_healthy_food_keyboard = types.InlineKeyboardMarkup()
confirm_healthy_food_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_healthy_food'))
confirm_healthy_food_keyboard.add(quit_back)

confirm_programming_keyboard = types.InlineKeyboardMarkup()
confirm_programming_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_programming'))
confirm_programming_keyboard.add(quit_back)

confirm_play_instruments_keyboard = types.InlineKeyboardMarkup()
confirm_play_instruments_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝',
                                                                 callback_data='select_play_instruments'))
confirm_play_instruments_keyboard.add(quit_back)

confirm_painting_keyboard = types.InlineKeyboardMarkup()
confirm_painting_keyboard.add(types.InlineKeyboardButton(text='Спорим 🤝', callback_data='select_painting'))
confirm_painting_keyboard.add(quit_back)
