# from admin.support_reviews.callbacks import Nums
# from db.models import Supt, User, RoundVideo
# from aiogram import types, Bot, Dispatcher
# from admin.support_reviews.messages import getQuestions
# from admin.support_reviews import keyboards, states
# from admin.states import AdminStates
# from client.initialize import bot as mainbot
#
#
import logging

from aiogram import Bot, Dispatcher, types

from admin.administration.states import AdministrationStates
from admin.administration.callbacks import show_admins
from db.models import DisputeAdmin

logger = logging.getLogger(__name__)


class Administration:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        pass

    def register_handlers(self):
        self.dp.register_message_handler(self.input_username_admin, state=AdministrationStates.input_username_admin)

    async def input_username_admin(self, message: types.Message):
        await AdministrationStates.none.set()
        DisputeAdmin.objects.create(username=message['text'])
        await message.answer("Готово!")

