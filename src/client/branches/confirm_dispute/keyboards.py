from aiogram import types

really_confirm_alcohol_keyboard = types.InlineKeyboardMarkup(row_width=2)
button1 = types.InlineKeyboardButton(text='👍 Есть / Куплю', callback_data='next_step_two')
# button2 = types.InlineKeyboardButton(text='Назад', callback_data='back_drink_smoke_drugs')
really_confirm_alcohol_keyboard.add(button1)

really_confirm_gym_keyboard = types.InlineKeyboardMarkup(row_width=2)
# button3 = types.InlineKeyboardButton(text='Назад', callback_data='sport_lose_weight')
really_confirm_gym_keyboard.add(button1)

really_confirm_morning_keyboard = types.InlineKeyboardMarkup(row_width=2)
first = types.InlineKeyboardButton(text='в 5:00', callback_data='five_am')
second = types.InlineKeyboardButton(text='в 6:00', callback_data='six_am')
third = types.InlineKeyboardButton(text='в 7:00', callback_data='seven_am')
fourth = types.InlineKeyboardButton(text='в 8:00', callback_data='eight_am')
really_confirm_morning_keyboard.add(first, second)
really_confirm_morning_keyboard.add(third, fourth)

all_confirm_keyboard = types.InlineKeyboardMarkup(row_width=2)
all_confirm_keyboard.add(types.InlineKeyboardButton(text='👍 Мне понятно', callback_data='agree'),
                         types.InlineKeyboardButton(text='Назад', callback_data='back_to_choice'))

really_confirm_language_keyboard = types.InlineKeyboardMarkup(row_width=2)
english = types.InlineKeyboardButton(text='Английский', callback_data='english')
chinese = types.InlineKeyboardButton(text='Китайский', callback_data='chinese')
spanish = types.InlineKeyboardButton(text='Испанский', callback_data='spanish')
arabian = types.InlineKeyboardButton(text='Арабский', callback_data='arabian')
italian = types.InlineKeyboardButton(text='Итальянский', callback_data='italian')
french = types.InlineKeyboardButton(text='Французский', callback_data='french')
really_confirm_language_keyboard.add(english, chinese)
really_confirm_language_keyboard.add(spanish, arabian)
really_confirm_language_keyboard.add(italian, french)

really_confirm_more_money_keyboard = types.InlineKeyboardMarkup(row_width=2)
hundred = types.InlineKeyboardButton(text='100 000 ₽', callback_data='hundred')
hundred3 = types.InlineKeyboardButton(text='300 000 ₽', callback_data='three_hundred')
really_confirm_more_money_keyboard.add(hundred, hundred3)
# really_confirm_more_money_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='more_money1'))

really_confirm_food_keyboard = types.InlineKeyboardMarkup(row_width=2)
button5 = types.InlineKeyboardButton(text='👍 Я понял/а', callback_data='agree_food')
# button6 = types.InlineKeyboardButton(text='Назад', callback_data='healthy_food1')
really_confirm_food_keyboard.add(button5)

really_confirm_programming_keyboard = types.InlineKeyboardMarkup(row_width=2)
button7 = types.InlineKeyboardButton(text='👍 Я понял/а', callback_data='agree_programming')
#button8 = types.InlineKeyboardButton(text='Назад', callback_data='programming1')
really_confirm_programming_keyboard.add(button7)

really_confirm_instruments_keyboard = types.InlineKeyboardMarkup(row_width=2)
piano = types.InlineKeyboardButton(text='Фортепиано', callback_data='piano')
guitar = types.InlineKeyboardButton(text='Гитаре', callback_data='guitar')
really_confirm_instruments_keyboard.add(piano, guitar)

really_confirm_painting_keyboard = types.InlineKeyboardMarkup(row_width=2)
pad = types.InlineKeyboardButton(text='На планшете', callback_data='pad')
hand = types.InlineKeyboardButton(text='От руки', callback_data='hand')
really_confirm_painting_keyboard.add(pad, hand)



no_promo_code_keyboard = types.InlineKeyboardMarkup()
no_promo_code_keyboard.add(types.InlineKeyboardButton(text='Без кода', callback_data='next_step_three'))

send_geo_position_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
send_geo_position_keyboard.add(types.KeyboardButton(text='Отправить гео 📍', callback_data='geo',
                                                    request_location=True))

test_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
test_keyboard.add(types.KeyboardButton(text='Отправить гео 📍', request_location=True))

choose_time_zone_keyboard = types.InlineKeyboardMarkup(row_width=4)

minus_ten_hour = types.InlineKeyboardButton(text='— 10:00', callback_data='— 10')
minus_half_nine_hour = types.InlineKeyboardButton(text='— 9:30', callback_data='— 9:30')
minus_nine_hour = types.InlineKeyboardButton(text='— 9:00', callback_data='— 9')
minus_eight_hour = types.InlineKeyboardButton(text='— 8:00', callback_data='— 8')

minus_seven_hour = types.InlineKeyboardButton(text='— 7:00', callback_data='— 7')
minus_six_hour = types.InlineKeyboardButton(text='— 6:00', callback_data='— 6')
minus_five_hour = types.InlineKeyboardButton(text='— 5:00', callback_data='— 5')
minus_four_hour = types.InlineKeyboardButton(text='— 4:00', callback_data='— 4')

minus_half_three_hour = types.InlineKeyboardButton(text='— 3:30', callback_data='— 3:30')
minus_three_hour = types.InlineKeyboardButton(text='— 3:00', callback_data='— 3')
minus_two_hour = types.InlineKeyboardButton(text='— 2:00', callback_data='— 2')
minus_one_hour = types.InlineKeyboardButton(text='— 1:00', callback_data='— 1')

zero_hour = types.InlineKeyboardButton(text='00:00', callback_data='+0')
plus_one_hour = types.InlineKeyboardButton(text='+1:00', callback_data='+1')
plus_two_hour = types.InlineKeyboardButton(text='+2:00', callback_data='+2')
plus_three_hour = types.InlineKeyboardButton(text='+3:00', callback_data='+3')

plus_half_three_hour = types.InlineKeyboardButton(text='+3:30', callback_data='+3:30')
plus_four_hour = types.InlineKeyboardButton(text='+4:00', callback_data='+4')
plus_half_four_hour = types.InlineKeyboardButton(text='+4:30', callback_data='+4:30')
plus_five_hour = types.InlineKeyboardButton(text='+5:00', callback_data='+5')

plus_half_five_hour = types.InlineKeyboardButton(text='+5:30', callback_data='+5:30')
plus_half15_five_hour = types.InlineKeyboardButton(text='+5:45', callback_data='+5:45')
plus_six_hour = types.InlineKeyboardButton(text='+6:00', callback_data='+6')
plus_half_six_hour = types.InlineKeyboardButton(text='+6:30', callback_data='+6:30')

plus_seven_hour = types.InlineKeyboardButton(text='+7:00', callback_data='+7')
plus_eight_hour = types.InlineKeyboardButton(text='+8:00', callback_data='+8')
plus_half_eight_hour = types.InlineKeyboardButton(text='+8:45', callback_data='+8:45')
plus_nine_hour = types.InlineKeyboardButton(text='+9:00', callback_data='+9')

plus_half_nine_hour = types.InlineKeyboardButton(text='+9:30', callback_data='+9:30')
plus_ten_hour = types.InlineKeyboardButton(text='+10:00', callback_data='+10')
plus_half_ten_hour = types.InlineKeyboardButton(text='+10:30', callback_data='+10:30')
plus_eleven_hour = types.InlineKeyboardButton(text='+11:00', callback_data='+11')

choose_time_zone_keyboard.add(minus_ten_hour, minus_half_nine_hour, minus_nine_hour, minus_eight_hour)
choose_time_zone_keyboard.add(minus_seven_hour, minus_six_hour, minus_five_hour, minus_four_hour)
choose_time_zone_keyboard.add(minus_half_three_hour, minus_three_hour, minus_two_hour, minus_one_hour)
choose_time_zone_keyboard.add(zero_hour, plus_one_hour, plus_two_hour, plus_three_hour)
choose_time_zone_keyboard.add(plus_half_three_hour, plus_four_hour, plus_half_four_hour, plus_five_hour)
choose_time_zone_keyboard.add(plus_half_five_hour, plus_half15_five_hour, plus_six_hour, plus_half_six_hour)
choose_time_zone_keyboard.add(plus_seven_hour, plus_eight_hour, plus_half_eight_hour, plus_nine_hour)
choose_time_zone_keyboard.add(plus_half_nine_hour, plus_ten_hour, plus_half_ten_hour, plus_eleven_hour)

alcohol_deposit_keyboard = types.InlineKeyboardMarkup()

alcohol_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
alcohol_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput1'))

smoking_deposit_keyboard = types.InlineKeyboardMarkup()
smoking_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
smoking_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput2'))

drugs_deposit_keyboard = types.InlineKeyboardMarkup()
drugs_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
drugs_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput3'))

gym_deposit_keyboard = types.InlineKeyboardMarkup()
gym_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
gym_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput4'))

weight_deposit_keyboard = types.InlineKeyboardMarkup()
weight_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
weight_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput5'))

morning_deposit_keyboard = types.InlineKeyboardMarkup()
morning_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
morning_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput6'))

language_deposit_keyboard = types.InlineKeyboardMarkup()
language_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
language_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput7'))

money_deposit_keyboard = types.InlineKeyboardMarkup()
money_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
money_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput8'))

food_deposit_keyboard = types.InlineKeyboardMarkup()
food_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
food_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput9'))

programming_deposit_keyboard = types.InlineKeyboardMarkup()
programming_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
programming_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput10'))

instruments_deposit_keyboard = types.InlineKeyboardMarkup()
instruments_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
instruments_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput11'))

painting_deposit_keyboard = types.InlineKeyboardMarkup()
painting_deposit_keyboard.add(types.InlineKeyboardButton(text='✅ Внести депозит', callback_data='make_deposit'))
painting_deposit_keyboard.add(types.InlineKeyboardButton(text='Редактировать', callback_data='edit_disput12'))
