from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile

from client.branches.confirm_dispute.messages import *
from client.branches.confirm_dispute.states import Promo
from client.tasks import reminder_scheduler_add_job, change_period_task_info
from db.models import User, BlogerPromocodes
from utils import get_timezone, get_date_to_start_dispute


class ConfirmDispute:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.input_promo_code_handler, state=Promo.input_promo)
        self.dp.register_message_handler(self.get_geo_position, content_types=['location'], state=Promo.geo_position)

    async def input_promo_code_handler(self, message: types.Message, state: FSMContext):

        blogers_promo = BlogerPromocodes.objects.all()
        is_blogger = False
        for i in range(len(blogers_promo)):
            if message.text == blogers_promo[i].promocode:
                blogers_promo[i].delete()
                await state.update_data(promocode=message.text, is_blogger=True, count_days=3, deposit='0')
                is_blogger = True
                await Promo.next()
                await message.answer(text='Спасибо 🙏 Промо-код успешно принят.')
                await message.answer(text=geo_position_msg, reply_markup=choose_time_zone_keyboard)
                break


        if User.objects.filter(promocode_user=message.text).exists():
            msg = 'Спасибо 🙏 Промо-код успешно принят.'
            await Promo.next()
            await state.update_data(promocode=message.text)
            await message.answer(text=msg)
            await message.answer(text=geo_position_msg, reply_markup=choose_time_zone_keyboard)
        else:
            if is_blogger is False:
                msg = 'Неверный промокод, попробуйте ещё раз'
                await message.answer(text=msg, reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(text='Без кода', callback_data='next_step_three')))

    async def get_geo_position(self, message: types.Message, state: FSMContext):

        loc = message.location
        # print(loc)
        tmp = get_timezone(loc)
        await state.update_data(timezone=tmp[:len(tmp) - 4])
        msg = f"Установлен часовой пояс {tmp}"

        await message.answer(text=msg)

        variant = await state.get_data()

        is_change_timezone = variant.get('is_change_timezone', None)

        if is_change_timezone:
            await change_period_task_info(message.from_user.id, tmp)

        else:
            await reminder_scheduler_add_job(self.dp, tmp[:len(tmp) - 4], "reminder", message.from_user.id, 1,
                                             notification_hour=10,
                                             notification_min=0)

        print(message.date)
        future_date = get_date_to_start_dispute(message.date, variant['start_disput'], tmp[:len(tmp) - 4])

        photo, choice_msg, tmp_keyboard = get_timezone_msg(future_date, variant)

        await message.answer_photo(photo=photo, caption=choice_msg, reply_markup=tmp_keyboard,
                                   parse_mode=ParseMode.MARKDOWN_V2)

        await state.update_data({'id_to_delete': message.message_id + 1})  # ??????? пофиксить
        if variant['is_blogger'] is True:
            await Promo.blogger.set()
        else:
            await Promo.none.set()