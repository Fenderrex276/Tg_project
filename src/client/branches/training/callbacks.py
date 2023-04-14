import uuid

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.types import ParseMode
from client.branches.training.keyboards import *
from client.branches.training.messages import *
from client.branches.training.states import Video
from client.initialize import dp
from client.tasks import del_scheduler, reminder_scheduler_add_job
from db.models import RoundVideo, User
from settings.settings import CHANNEL_ID


async def preparation_for_dispute(call: types.CallbackQuery, state: FSMContext):
    await Video.none.set()
    await state.update_data(id_dispute=uuid.uuid4().time_mid)
    data = await state.get_data()
    links_msgs = ['alcohol', 'smoking', 'drugs']
    photo = InputFile("client/media/training/algorithm.jpg")
    await call.message.answer_photo(photo=photo, caption=algorithm_msg)
    if data['action'] in links_msgs:
        await call.message.answer(text=message_to_prepare(data), reply_markup=test_confirm_keyboard,
                                  parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await call.message.answer(text=message_to_prepare(data), reply_markup=test_confirm_keyboard)
    await call.answer()


async def send_video_note(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    tmp_msg, video = message_to_training(data)

    await call.message.answer(tmp_msg)

    if data['action'] == 'money':
        await call.bot.send_video(call.message.chat.id, video, reply_markup=None)
        await Video.recv_video.set()
    else:
        await Video.recv_video_note.set()
        await call.bot.send_video_note(call.message.chat.id, video, reply_markup=None)
    await call.answer()


async def send_video_to_admin(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    print(v)

    await RoundVideo.objects.acreate(tg_id=v['video_id'],
                                     user_tg_id=call.from_user.id,
                                     chat_tg_id=call.message.chat.id,
                                     code_in_video="3028",
                                     id_video=v['id_dispute'],
                                     type_video=RoundVideo.TypeVideo.test)

    tmp_msg = "🎈 Спасибо, репорт успешно отправлен на верификацию. Ожидайте результатов проверки."

    print("FROM USER_BOT", v['video_id'])
    print("CHAT_ID", call.message.chat.id)
    await Video.next_step.set()
    await call.message.answer(text=tmp_msg)
    await call.bot.send_video_note(video_note=v['video_id'], chat_id=CHANNEL_ID)
    await call.answer()

    # scheduler_add_job(dp, 'reminder', call.from_user.id, 7)


async def send_new_video(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['action'] == 'money':
        await Video.recv_video.set()
    else:
        await Video.recv_video_note.set()
    tmp_msg = "Отправь новое видео, на котором чётко слышан код"
    await call.message.answer(text=tmp_msg)
    await call.answer()


async def pin_a_chat(call: types.CallbackQuery):
    photo = InputFile("client/media/training/done.jpg")
    await call.message.answer_photo(photo=photo, caption=pin_chat_msg, reply_markup=success_pin_keyboard)
    await call.answer()


async def end_test_dispute(call: types.CallbackQuery, state: FSMContext):
    photo = InputFile("client/media/training/end_test.jpg")
    msg = "Поздравляем! Теперь ты сможешь добиться любой своей цели. Удачи 😉"
    await state.update_data(id_video_code="")
    await call.message.answer_photo(photo=photo, caption=msg, reply_markup=go_to_dispute_keyboard)
    await call.answer()


async def new_support_question(call: types.CallbackQuery, state: FSMContext):
    await Video.new_question.set()

    await call.message.answer(text='💬 Введи сообщение:')
    await call.answer()


def register_callback(bot, dp: Dispatcher):
    dp.register_callback_query_handler(preparation_for_dispute, text='step_to_test_video_note', state="*")
    dp.register_callback_query_handler(send_video_note, text='next_one', state=Video.none)
    dp.register_callback_query_handler(send_video_note, text='lets_start_training', state="*")
    dp.register_callback_query_handler(send_video_to_admin, text='send_video', state=Video.recv_video)
    dp.register_callback_query_handler(send_video_to_admin, text='send_video', state=Video.recv_video_note)
    dp.register_callback_query_handler(send_new_video, text='send_new_video', state=Video.recv_video)
    dp.register_callback_query_handler(send_new_video, text='send_new_video', state=Video.recv_video_note)
    dp.register_callback_query_handler(send_new_video, text='send_new1', state=Video.all_states)
    dp.register_callback_query_handler(send_new_video, text='send_new1', state=Video.all_states)
    dp.register_callback_query_handler(pin_a_chat, text='good', state=Video.next_step)
    dp.register_callback_query_handler(end_test_dispute, text='end_test', state=Video.next_step)
    dp.register_callback_query_handler(send_new_video, text='next_one1', state=Video.recv_video)
    dp.register_callback_query_handler(send_new_video, text='next_one1', state=Video.recv_video_note)
    dp.register_callback_query_handler(new_support_question, text='podderzka', state=Video.recv_video)
    dp.register_callback_query_handler(new_support_question, text='podderzka', state=Video.recv_video_note)
