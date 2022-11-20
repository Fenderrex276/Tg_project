from db.models import Supt, Users, RoundVideo
from aiogram import types
from admin.support_reviews.messages import getQuestions
from admin.support_reviews import keyboards


async def write_quest(num_review, message: types.Message):
    num_review += 1
    sup = await Supt.objects.filter(solved="new").afirst()
    try:
        nds = await RoundVideo.objects.filter(user_tg_id=sup.user_id).alast().n_days
    except:
        nds = "0"
    nd = await Users.objects.filter(user_id=sup.user_id).afirst()
    await message.answer(getQuestions(num_review, nd.number_dispute, nds, sup.problem),
                         reply_markup=keyboards.review_keyboard)
