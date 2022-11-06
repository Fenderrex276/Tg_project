from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile
from .keyboards import *
from .states import StatesDispute
from .callbacks import video_text


class CurrentDispute:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        ...

    def register_handlers(self):
        self.dp.register_message_handler(self.the_hero_path, text=[menu_keyboard, "✅ Путь героя"],
                                         state=StatesDispute.all_states)
        self.dp.register_message_handler(self.knowledge_base, text=[menu_keyboard, "💚 База знаний"],
                                         state=StatesDispute.all_states)
        self.dp.register_message_handler(self.account, text=[menu_keyboard, "🟢 Аккаунт"],
                                         state=StatesDispute.all_states)

        self.dp.register_message_handler(self.process_name_invalid, lambda message: len(message.text) > 20,
                                         state=StatesDispute.change_name)

        self.dp.register_message_handler(self.input_name, state=StatesDispute.change_name)

    async def the_hero_path(self, message: types.Message, state: FSMContext):
        await StatesDispute.none.set()
        data = await state.get_data()
        print(data)
        recieve_message = video_text(data)
        await state.update_data(name=message.from_user.first_name)

        await message.answer_photo(photo=InputFile(recieve_message[0]))
        await message.answer(text=recieve_message[1], reply_markup=report_diary_keyboard,
                             parse_mode=ParseMode.MARKDOWN)

    async def knowledge_base(self, message: types.Message):
        await StatesDispute.knowledge_base.set()
        msg = ("*💚 База знаний* \n\n"
               "Читайте о том, как живут и работают самые успешные люди планеты, сохраняйте уникальные мемы,"
               " знакомьтесь с великими книгами и смотрите хорошее кино, чтобы больше узнать о том, "
               "как легче и проще добиваться своих целей, сохранять фокус и мотивацию:")

        await message.answer(text=msg, reply_markup=knowledge_base_keyboard, parse_mode=ParseMode.MARKDOWN_V2)

    async def account(self, message: types.Message, state: FSMContext):
        await StatesDispute.account.set()
        user = await state.get_data()
        msg = (f"👋 *Привет, {user['name']}* \n\n"
               "Здесь ты можешь изменить своё имя, вывести выигранный депозит, "
               "изменить свой часовой пояс или написать свой вопрос в тех. "
               "поддержку через форму обратной связи.")

        await message.answer(text=msg, reply_markup=account_keyboard, parse_mode=ParseMode.MARKDOWN)

    async def input_name(self, message: types.Message, state: FSMContext):
        await StatesDispute.account.set()
        await state.update_data(name=message.text)

        await message.answer(text='Готово!')

    async def process_name_invalid(self, message: types.Message):
        msg = "Максимум 20 символов, пожалуйста попробуйте ещё раз"
        return await message.answer(msg)
