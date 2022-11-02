# from utils import datetime_to_miliseconds
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from branches.dispute_with_friend.messages import dispute_choice_msg
from branches.dispute_with_friend.keyboards import thirty_days_keyboard
from branches.dispute_with_friend.states import Form
from branches.start.keyboards import menu_keyboard


class DisputeWithFriend:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        # команды
        self.dp.register_message_handler(self.dispute_handler, text=[menu_keyboard, "🤜 Спорим 🤛"], state="*")
        self.dp.register_message_handler(self.dispute_handler, text=[menu_keyboard, "🤜 Спорим 🤛"])

    def register_handlers(self):
        ...

    async def dispute_handler(self, message: types.Message):
        await self.bot.send_message(message.from_user.id, dispute_choice_msg, parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=thirty_days_keyboard)
