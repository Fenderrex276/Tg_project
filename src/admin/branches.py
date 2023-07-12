import logging

from aiogram import Bot

from admin.support_reviews.states import ReviewStates
from db.models import RoundVideo, DisputeAdmin
from settings.settings import SUPER_ADMIN
from .administration.states import AdministrationStates
from .keyboards import support_menu_keyboard
from admin.administration.keyboards import administration_menu_keyboard
from .states import AdminStates
from .сallbacks import *

logger = logging.getLogger(__name__)


# TODO На каждую кнопку повесить проверку доступа
class Admin:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.start_handler, commands=["start"], state='*')
        self.dp.register_message_handler(self.start_handler, text=["start"], state='*')
        self.dp.register_message_handler(self.reports, text=f"✅ Репорты", state="*")
        self.dp.register_message_handler(self.supports, text=f"💚 Поддержка и отзывы", state="*")
        self.dp.register_message_handler(self.administration, text=f"‍👤 Администрирование", state="*")

    async def start_handler(self, message: types.Message, state: FSMContext):
        username = message['from']['username']
        try:
            admin = DisputeAdmin.objects.get(username=username)
            is_super = admin.is_super_admin
            if admin.user_id is None:
                admin.user_id = message['from']['id']
                admin.chat_id = message['chat']['id']
                admin.save()
            if not admin.is_active:
                await self.bot.send_message(message['from']['id'], text=f"У вас нет доступа")
                return
        except DisputeAdmin.DoesNotExist:
            if SUPER_ADMIN != username:
                await self.bot.send_message(message['from']['id'], text=f"У вас нет доступа")
                return
            is_super = True
        text = f'Меню админа'
        admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

        admin_menu.add(types.KeyboardButton(f"✅ Репорты"))
        admin_menu.add(types.KeyboardButton(f"💚 Поддержка и отзывы"))
        if is_super:
            admin_menu.add(types.KeyboardButton(f"‍👤 Администрирование"))
            text = f'Меню супер-админа'

        await self.bot.send_message(message['from']['id'], text, reply_markup=admin_menu)
        await AdminStates.is_admin.set()

    async def reports(self, message: types.Message, state: FSMContext):
        dispute_videos = RoundVideo.objects.exclude(tg_id__isnull=True).filter(status="",
                                                                               type_video=RoundVideo.TypeVideo.dispute)

        test_videos = RoundVideo.objects.exclude(tg_id__isnull=True).filter(status="",
                                                                            type_video=RoundVideo.TypeVideo.test)

        reports_menu_keyboard = types.InlineKeyboardMarkup()
        reports_menu_keyboard.add(
            types.InlineKeyboardButton(text=f"Ежедневные ({len(dispute_videos)})", callback_data="every_day"))
        reports_menu_keyboard.add(
            types.InlineKeyboardButton(text=f"Тестовые ({len(test_videos)})", callback_data="test_videos"))
        reports_menu_keyboard.add(types.InlineKeyboardButton(text="До результата (0)", callback_data="before_result"))
        reports_menu_keyboard.add(types.InlineKeyboardButton(text="Архив", callback_data="archive"))

        await message.answer(text="Меню репортов", reply_markup=reports_menu_keyboard)

    async def supports(self, message: types.Message, state: FSMContext):
        await message.answer(text="💚 Поддержка и отзывы", reply_markup=support_menu_keyboard)
        await ReviewStates.none.set()

    async def administration(self, message: types.Message, state: FSMContext):
        await message.answer(text=f"Администрирование", reply_markup=administration_menu_keyboard)
        await AdministrationStates.none.set()
