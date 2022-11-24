from admin.support_reviews.callbacks import Nums
from db.models import Supt, Users, RoundVideo
from aiogram import types, Bot, Dispatcher
from admin.support_reviews.messages import getQuestions
from admin.support_reviews import keyboards, states
from admin.states import AdminStates
from initialize import bot as mainbot


class Reviews:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        pass

    def register_handlers(self):
        self.dp.register_message_handler(self.input_review, state=states.ReviewStates.input_review)
        self.dp.register_message_handler(self.input_pass_review, state=states.ReviewStates.input_pass_review)
        self.dp.register_message_handler(self.write_archive, state=states.ReviewStates.archive)

    async def input_review(self, message: types.Message):
        await states.ReviewStates.none.set()
        sup = await Supt.objects.filter(solved="new").afirst()
        await mainbot.send_message(text="Ваша заявка расмотрена:\n\n" + message.text, chat_id=sup.chat_id)
        sup.solved = "done"
        sup.save()
        await message.answer("Готово!")

    async def input_pass_review(self, message: types.Message):
        await states.ReviewStates.none.set()
        sup = await Supt.objects.filter(solved="in_process").afirst()
        await mainbot.send_message(text="Ваша заявка расмотрена:\n\n" + message.text, chat_id=sup.chat_id)
        sup.solved = "done"
        sup.save()
        await message.answer("Готово!")

    async def write_archive(self, message: types.Message):
        try:
            s = Supt.objects.filter(number_dispute=message.text, solved="done").all()
            if s.count() > 0:
                for sup in s:
                    try:
                        nds = RoundVideo.objects.filter(user_tg_id=sup.user_id).last().n_day
                    except:
                        nds = "0"
                    nd = await Users.objects.filter(user_id=sup.user_id).afirst()
                    await message.answer(getQuestions(Nums.num_review, nd.number_dispute, nds, sup.problem))
            else:
                await message.answer("Диспут не найден. Скопируй номер диспута и введи (#D****):")
        except:
            await message.answer("Диспут не найден. Скопируй номер диспута и введи (#D****):")


async def write_quest(num_review, message: types.Message):
    try:
        sup = await Supt.objects.filter(solved="new").afirst()
        try:
            nds = RoundVideo.objects.filter(user_tg_id=sup.user_id).last().n_days
        except:
            nds = "0"
        nd = await Users.objects.filter(user_id=sup.user_id).afirst()
        await message.answer(getQuestions(num_review, nd.number_dispute, nds, sup.problem),
                             reply_markup=keyboards.review_keyboard)
    except:
        await message.answer("Упс... Новых обращений в поддержку нет")


async def write_pass_quest(num_review, num_pass, message: types.Message):
    try:
        s = Supt.objects.filter(solved="in_process")
        sup = s[num_pass]
        try:
            nds = RoundVideo.objects.filter(user_tg_id=sup.user_id).last().n_days
        except:
            nds = "0"
        nd = await Users.objects.filter(user_id=sup.user_id).afirst()
        await message.answer(getQuestions(num_review, nd.number_dispute, nds, sup.problem),
                             reply_markup=keyboards.review_pass_keyboard)
    except:
        await message.answer("Упс... Отложенных обращений в поддержку нет")
