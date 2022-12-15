from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.types import InputFile, ParseMode
from client.branches.dispute_with_friend.states import Form
from client.branches.knowledge_base.FAQ import messages, keyboards
from client.branches.start.keyboards import *
from client.branches.start.messages import first_faq_msg
from client.branches.knowledge_base.FAQ.callbacks import choose_faq
from client.branches.thirty_days_dispute.states import StatesDispute


class Start:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        # команды
        self.dp.register_message_handler(self.start_handler, commands=["start"])

        self.dp.register_message_handler(self.faq_handler, text=[menu_keyboard, "🫀FAQ"], state="*")
        self.dp.register_message_handler(self.reviews, text=[menu_keyboard, "👍Отзывы"], state="*")

    def register_handlers(self):
        ...

    async def start_handler(self, message: types.Message):
        # check user in data
        # print(message.text)
        await Form.none.set()
        msg = ("⛅ Ежедневная работа даёт результат абсолютно в любом деле. А мотивация не потерять свой"
               " депозит работает так же сильно, как мотивация заработать 💰\n\n"
               "Простые правила игры:\n"
               "🍎 Определи свою цель и внеси депозит\n"
               "⏰ Отправляй в бот короткие видео с уникальным кодом, как доказательство процесса и результата\n"
               "👍 Если все ок, игра продолжится и вы сохраните свой депозит\n"
               "👎 Если правила спора нарушены, вы проиграете сначала 20% депозита,"
               " а если это повторится — остальные 80%.\n\n"
               "Пройди ✅ путь Героя и открой новый мир своих личных возможностей, здоровые привычки, новых друзей,"
               " поддержку и яркие эмоции.")

        await self.bot.send_message(
            message.from_user.id, msg, reply_markup=menu_keyboard)

    async def faq_handler(self, message: types.Message):
        await StatesDispute.account.set()
        await self.bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        await message.answer(text=messages.start_FAQ, reply_markup=keyboards.start_md_keyboard,
                                  parse_mode=ParseMode.MARKDOWN)


    async def reviews(self, message: types.Message):
        msg = "Читайте отзывы пользователей об игре и их личном опыте на нашем телеграмм-канале:"

        await self.bot.send_message(message.from_user.id, text=msg, reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text="Открыть", url="https://t.me/DisputeGame")))
