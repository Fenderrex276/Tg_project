from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from admin.reports.callbacks import test_videos
from db.models import RoundVideo
from initialize import bot as mainbot
from admin.reports.states import ReportStates


class Reports:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.input_message, state=ReportStates.input_message)

    async def input_message(self, message: types.Message, state: FSMContext):
        v = await state.get_data()
        RoundVideo.objects.filter(tg_id=v['video_user_id']).update(status="bad")
        user = RoundVideo.objects.get(tg_id=v['video_user_id'])

        await mainbot.send_message(text=message.text,
                                   chat_id=user.chat_tg_id,
                                   reply_markup=types.InlineKeyboardMarkup().add(
                                       types.InlineKeyboardButton(text='Отправить репорт', callback_data="send_new1")
                                   ))
        await ReportStates.none.set()
        await message.answer("Готово!")

