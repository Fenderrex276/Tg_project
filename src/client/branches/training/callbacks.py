import uuid

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.types import ParseMode


from client.branches.training.keyboards import *
from client.branches.training.messages import *
from client.branches.training.states import Video
from client.initialize import dp
from client.tasks import del_scheduler, reminder_scheduler_add_job, init_send_code
from db.models import RoundVideo, User
from settings.settings import CHANNEL_ID
from admin.initialize import bot as adminbot


async def preparation_for_dispute(call: types.CallbackQuery, state: FSMContext):
    await Video.none.set()
    await state.update_data(id_dispute=uuid.uuid4().time_mid)
    data = await state.get_data()
    links_msgs = ['alcohol', 'smoking', 'drugs']
    photo = InputFile("client/media/training/algorithm.jpg")
    await call.message.answer_photo(photo=photo, caption=algorithm_msg)
    if data['action'] in links_msgs:
        await call.message.answer(text=message_to_prepare(data), reply_markup=test_confirm_keyboard,
                                  parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
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
    await adminbot.send_message(text='У вас новый кружок на проверку в разделе "тестовые', chat_id=-792408904)
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


async def monday_or_after_tomorrow(call: types.CallbackQuery, state: FSMContext):
    # print(call.data)
    # await state.update_data(start_disput=call.data)
    await Video.date.set()
    data = await state.get_data()
    round_video_info = await RoundVideo.objects.aget(tg_id=data['video_id'])

    try:
        user = await User.objects.filter(user_id=call.from_user.id).alast()
    except User.DoesNotExist:
        print("Пользователь не найден")
        return


    start = ""
    data_start = ""

    if call.data == "select_after_tomorrow":
        start = "послезавтра"
        data_start = "tomorrow"
    elif call.data == "select_monday":
        start = "в понедельник"
        data_start = "monday"

    user.start_disput = data_start
    user.save()
    # TODO SIM вот твоя функция в клиентской части
    await init_send_code(round_video_info.user_tg_id, round_video_info.chat_tg_id, start, round_video_info.id_video,
                         user.timezone, 4, 30)
    # TODO SIM короче я сюда эту функцию добавил

    await call.message.answer(text=f"Твой новый код придёт сюда {start}.", reply_markup=success_keyboard)
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
    dp.register_callback_query_handler(pin_a_chat, text='good', state=Video.date)
    dp.register_callback_query_handler(end_test_dispute, text='end_test', state=Video.date)
    dp.register_callback_query_handler(send_new_video, text='next_one1', state=Video.recv_video)
    dp.register_callback_query_handler(send_new_video, text='next_one1', state=Video.recv_video_note)
    dp.register_callback_query_handler(new_support_question, text='podderzka', state=Video.recv_video)
    dp.register_callback_query_handler(new_support_question, text='podderzka', state=Video.recv_video_note)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='select_after_tomorrow', state=Video.next_step)
    dp.register_callback_query_handler(monday_or_after_tomorrow, text='select_monday', state=Video.next_step)
