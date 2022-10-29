from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile
from branches.training.messages import *
from branches.training.keyboards import *
from branches.training.states import Video


async def preparation_for_dispute(call: types.CallbackQuery):

    photo = InputFile("media/training/algorithm.jpg")
    await call.message.answer_photo(photo=photo)
    await call.message.answer(text=algorithm_msg)
    await call.message.answer(text=algorithm_msg2, reply_markup=test_confirm_keyboard)


async def send_video_note(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    video = InputFile
    tmp_msg = ""
    if data['action'] == 'alcohol':
        tmp_msg = send_video_alcohol_msg
        video = InputFile("media/videos/alcohol.mp4")
    elif data['action'] == 'drugs':
        tmp_msg = send_video_drugs_msg
        video = InputFile("media/videos/drugs.mp4")
    elif data['action'] == 'smoking':
        tmp_msg = send_video_smoking_msg
        video = InputFile("media/videos/smoke.mp4")
    elif data['action'] == 'gym':
        tmp_msg = send_video_gym_msg
        video = InputFile("media/videos/gym.mp4")
    elif data['action'] == 'weight':
        tmp_msg = send_video_weight_msg
        video = InputFile("media/videos/weight.mp4")
    elif data['action'] == 'morning':
        tmp_msg = send_video_morning_msg
        video = InputFile("media/videos/morning.mp4")
    elif data['action'] == 'language':
        tmp_msg = send_video_language_msg
        video = InputFile("media/videos/language.mp4")
    elif data['action'] == 'money':
        tmp_msg = send_video_bank_msg
        video = InputFile("media/videos/bank.mp4")
    elif data['action'] == 'food':
        tmp_msg = send_video_food_msg
        video = InputFile("media/videos/food.mp4")
    elif data['action'] == 'programming':
        tmp_msg = send_video_programming_msg
        video = InputFile("media/videos/programming.mp4")
    elif data['action'] == 'instruments':
        tmp_msg = send_video_instrument_msg
        video = InputFile("media/videos/piano.mp4")
    elif data['action'] == 'painting':
        tmp_msg = send_video_painting_msg
        video = InputFile("media/videos/painting.mp4")

    await call.message.answer(tmp_msg)

    if data['action'] == 'money':
        await call.bot.send_video(call.message.chat.id, video, reply_markup=None)
        await Video.recv_video.set()
    else:
        await Video.recv_video_note.set()
        await call.bot.send_video_note(call.message.chat.id, video, reply_markup=None)


async def send_video_to_admin(call: types.CallbackQuery, state: FSMContext):

    tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."
    await Video.none.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.ReplyKeyboardRemove())


async def send_new_video(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Отправь новое видео, на котором чётко слышан код"
    await call.message.answer(text=tmp_msg)


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(preparation_for_dispute, text='step_to_test_video_note', state="*")
    dp.register_callback_query_handler(send_video_note, text='next_one', state="*")
    dp.register_callback_query_handler(send_video_to_admin, text='send_video', state=Video.recv_video)
    dp.register_callback_query_handler(send_video_to_admin, text='send_video', state=Video.recv_video_note)
    dp.register_callback_query_handler(send_new_video, text='send_new_video', state=Video.recv_video)
    dp.register_callback_query_handler(send_new_video, text='send_new_video', state=Video.recv_video_note)
