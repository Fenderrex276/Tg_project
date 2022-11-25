from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile

from client.branches.pay.messages import *
from client.branches.pay.states import PayStates
from client.branches.start.keyboards import menu_keyboard
from client.branches.confirm_dispute.states import Promo
from client.branches.confirm_dispute.keyboards import *
from utils import get_timezone, get_date_to_start_dispute
from client.branches.pay.keyboards import *


class Pay:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.input_other_sum, state=PayStates.input_sum)

    async def input_other_sum(self, message: types.Message, state: FSMContext):

        if int(message.text) > 150000:
            await message.answer(text='Сумма не должна превышать 150 000 ₽')
        elif int(message.text) < 15000:
            await message.answer(text='Сумма должна быть не менее 15 000 ₽')
        else:
            print('Готово')
            await state.update_data(deposit=message.text)
            await PayStates.none.set()
            await message.answer(text=application_for_payment_msg, reply_markup=get_banking_detials_keyboard)
