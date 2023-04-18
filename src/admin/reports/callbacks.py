import logging
from random import randint

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from admin.keyboards import *
from admin.reports.states import ReportStates
from admin.сallbacks import current_dispute
from client.initialize import bot as mainbot
from client.tasks import del_scheduler
from db.models import RoundVideo, User

logger = logging.getLogger(__name__)


async def test_videos(call: types.CallbackQuery, state: FSMContext):
    new_video = await RoundVideo.objects.exclude(tg_id__isnull=True).filter(
        status="",
        type_video=RoundVideo.TypeVideo.test,
    ).afirst()

    if new_video is None or new_video.tg_id == "":
        await call.message.answer("Нет новых видео")
    else:
        user = await User.objects.filter(user_id=new_video.user_tg_id).afirst()
        print(user.action, user.additional_action)

        id_dispute = str(new_video.id_video)
        purpose = current_dispute(user.action, user.additional_action)

        code = " ".join(list(new_video.code_in_video))

        tmp_msg = (f"Диспут #D{id_dispute}\n"
                   f"*День 0*\n\n"
                   f"🔒 {code}\n"
                   f"{purpose}")

        await state.update_data(video_user_id=new_video.tg_id, user_id=call.from_user.id, id_video=new_video.id_video)
        await call.message.answer(text=tmp_msg, parse_mode=ParseMode.MARKDOWN)
        if user.action == "money":
            await call.message.answer_video(video=new_video.tg_id,
                                            reply_markup=test_keyboard)
        else:
            await call.message.answer_video_note(video_note=new_video.tg_id,
                                                 reply_markup=test_keyboard)
    await call.answer()


async def access_video(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await RoundVideo.objects.filter(tg_id=data['video_user_id']).aupdate(status="good",
                                                                         type_video=RoundVideo.TypeVideo.archive)

    await call.message.answer(text="Готово!")

    round_video_info = await RoundVideo.objects.aget(tg_id=data['video_user_id'])

    select_day_keyboard = types.InlineKeyboardMarkup(row_width=2)
    monday_button = types.InlineKeyboardButton(text='С понедельника', callback_data='select_monday')
    after_tomorrow_button = types.InlineKeyboardButton(text='👍 Послезавтра', callback_data='select_after_tomorrow')
    select_day_keyboard.add(after_tomorrow_button, monday_button)

    await mainbot.send_message(text="Отлично 🔥 У тебя всё получилось", chat_id=round_video_info.chat_tg_id)
    await mainbot.send_message(text=f"Диспут продлится каждый из 30 последующих дней,"
                                    f" без возможности прерваться. Когда вы готовы начать?",
                               chat_id=round_video_info.chat_tg_id,
                               reply_markup=select_day_keyboard)

    await test_videos(call, state)
    await call.answer()


async def refused_video(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=refused_keyboard)
    await call.answer()


async def new_code(chat_id: int, user_id, id_video):
    new_code = str(randint(1000, 9999))
    code = " ".join(list(new_code))
    msg = f"Твой новый код: {code}"

    user = await User.objects.filter(user_id=user_id).alast()
    user.count_days = user.count_days - 1
    print("USER AFTER CODE : ", user.count_days)
    user.save()
    print("USER DAY IN VIDEO CODE : ", 30 - user.count_days)

    await RoundVideo.objects.acreate(user_tg_id=user_id,
                                     chat_tg_id=chat_id,
                                     code_in_video=new_code,
                                     id_video=id_video,
                                     type_video=RoundVideo.TypeVideo.dispute,
                                     n_day=(30 - user.count_days))

    await mainbot.send_message(text=msg, chat_id=chat_id, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Отправить репорт", callback_data="send_dispute_report")),
                               disable_notification=True)


async def thirty_days_videos(call: types.CallbackQuery):
    tmp_msg = "Сюда попадают новые репорты из 30 дневной игры \"Испытания воли\""

    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='🔥 Начать', callback_data='lets_go'),
        types.InlineKeyboardButton(text='Назад', callback_data='back_reports')))
    await call.answer()


async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(text="Меню репортов", reply_markup=reports_menu_keyboard)
    await call.answer()


async def back_to_video(call: types.CallbackQuery):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    await call.answer()


async def confirm_video(call: types.CallbackQuery):
    await call.message.answer(text='Пользователь успешно прошел подготовку и готов к игре?',
                              reply_markup=access_keyboard)
    await call.answer()


async def refused1_video(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    await RoundVideo.objects.filter(tg_id=v['video_user_id']).aupdate(status="bad",
                                                                      type_video=RoundVideo.TypeVideo.archive)

    user = await RoundVideo.objects.aget(tg_id=v['video_user_id'])

    await mainbot.send_message(text=" Не видно лица / результатов. Пожалуйста, попробуй ещё раз",
                               chat_id=user.chat_tg_id,
                               reply_markup=types.InlineKeyboardMarkup().add(
                                   types.InlineKeyboardButton(text='Отправить репорт', callback_data="send_new1")
                               ))

    await call.message.answer('Готово!')
    await test_videos(call, state)
    await call.answer()


async def refused2_video(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    await RoundVideo.objects.filter(tg_id=v['video_user_id']).aupdate(status="bad",
                                                                      type_video=RoundVideo.TypeVideo.archive)
    user = await RoundVideo.objects.aget(tg_id=v['video_user_id'])

    await mainbot.send_message(text="На видео не слышно кода. Пожалуйста, попробуй ещё раз",
                               chat_id=user.chat_tg_id,
                               reply_markup=types.InlineKeyboardMarkup().add(
                                   types.InlineKeyboardButton(text='Отправить репорт', callback_data="send_new1")
                               ))

    await call.message.answer('Готово!')


async def refused3_video(call: types.CallbackQuery, state: FSMContext):
    await ReportStates.input_message.set()

    await call.message.answer("Введите сообщение:")
    await call.answer()


async def archive_button(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи номер Диспута (#D****)"
    await ReportStates.input_id_dispute.set()
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_archive")
    ))
    await call.answer()


async def thirty_day_dispute(call: types.CallbackQuery, state: FSMContext):
    new_dispute = await RoundVideo.objects.exclude(tg_id__isnull=True).filter(
        status="",
        type_video=RoundVideo.TypeVideo.dispute,
    ).afirst()

    if new_dispute is None or new_dispute.tg_id == "":
        await call.message.answer("Нет новых видео")
    else:
        user = await User.objects.filter(user_id=new_dispute.user_tg_id).afirst()
        id_dispute = str(new_dispute.id_video)
        purpose = current_dispute(user.action, user.additional_action)

        code = " ".join(list(new_dispute.code_in_video))

        tmp_msg = (f"Диспут #D{id_dispute}\n"
                   f"*День {new_dispute.n_day}*\n\n"
                   f"🔒 {code}\n"
                   f"{purpose}")

        await state.update_data(video_user_id=new_dispute.tg_id, user_id=call.from_user.id,
                                id_video=new_dispute.id_video)
        await call.message.answer(text=tmp_msg, parse_mode=ParseMode.MARKDOWN)
        if user.action == "money":
            await call.message.answer_video(video=new_dispute.tg_id,
                                            reply_markup=volya_keyboard)
        else:
            await call.message.answer_video_note(video_note=new_dispute.tg_id,
                                                 reply_markup=volya_keyboard)
    await call.answer()


async def accept_current_dispute(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "На видео один и тот же человек по голосу?"

    data = await state.get_data()
    current_video = await RoundVideo.objects.filter(tg_id=data['video_user_id']).afirst()
    start_video = await RoundVideo.objects.filter(
        user_tg_id=current_video.user_tg_id,
        n_day=0,
        status="good",
    ).afirst()
    await call.message.answer_video_note(video_note=start_video.tg_id)
    await call.message.answer(text=tmp_msg, reply_markup=access_volya_keyboard)
    await call.answer()
    del_scheduler(job_id=f'{current_video.user_tg_id}_soft_deadline_reminder', where='admin')
    del_scheduler(job_id=f'{current_video.user_tg_id}_hard_deadline_reminder', where='admin')


async def access_volya_dispute(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await RoundVideo.objects.filter(tg_id=data['video_user_id']).aupdate(status="good",
                                                                         type_video=RoundVideo.TypeVideo.archive)

    await call.message.answer(text="Готово!")

    video_user = await RoundVideo.objects.filter(tg_id=data['video_user_id']).alast()

    await mainbot.send_message(text="Отлично 🔥 У тебя всё получилось", chat_id=video_user.chat_tg_id)
    await mainbot.send_message(text="Твой новый код придёт сюда завтра.", chat_id=video_user.chat_tg_id,
                               reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
                                   text='Отлично!', callback_data="nice_god_job")))

    user = await User.objects.aget(user_id=video_user.user_tg_id)

    if user.count_days == 0:
        del_scheduler(job_id=f'{video_user.user_tg_id}_send_code', where='admin')
    """reply_markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Отлично!', callback_data='nice_go_next')
    )"""

    data = await state.get_data()
    await thirty_day_dispute(call, state)
    await call.answer()


async def refused_video_thirty_day(call: types.CallbackQuery, state: FSMContext):
    v = await state.get_data()
    await RoundVideo.objects.filter(tg_id=v['video_user_id']).aupdate(status="bad",
                                                                      type_video=RoundVideo.TypeVideo.archive)

    user = await RoundVideo.objects.aget(tg_id=v['video_user_id'])
    id_user = user.user_tg_id
    tmp = await User.objects.filter(user_id=user.user_tg_id).alast()

    tmp.count_mistakes = tmp.count_mistakes - 1
    # TODO добавить библу с деньгами
    if tmp.count_mistakes == 1:
        tmp.deposit = round(tmp.deposit - tmp.deposit / 5)
    elif tmp.count_mistakes == 0:
        tmp.deposit = 0
        del_scheduler(job_id=f'{user.user_tg_id}_send_code', where='admin')
    tmp.save()
    await mainbot.send_message(text="⛔️ Несоответствие условиям спора",
                               chat_id=user.chat_tg_id, reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='👍 Больше не повторится', callback_data='try_again')
        ))

    await call.message.answer('Готово!')
    await thirty_day_dispute(call, state)
    del_scheduler(job_id=f'{user.chat_tg_id}_soft_deadline_reminder', where='admin')
    del_scheduler(job_id=f'{user.chat_tg_id}_hard_deadline_reminder', where='admin')

    await call.answer()


async def ninety_day_volya(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Сюда попадают новые репорты из 90 дневной игры \"Личные цели\""

    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="🔥 Начать", callback_data="start_volya"),
        types.InlineKeyboardButton(text="Назад", callback_data="back_from_volya")
    ))
    await call.answer()


async def new_videos_volya(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Новых репортов в категории “Личные цели” не обнаружено."

    await call.message.answer(text=tmp_msg)
    await call.answer()


def register_callback(dp: Dispatcher, bot: Bot):
    dp.register_callback_query_handler(test_videos, text='test_videos', state="*")
    dp.register_callback_query_handler(access_video, text='confirm_video', state="*")
    dp.register_callback_query_handler(confirm_video, text='good', state="*")
    dp.register_callback_query_handler(refused_video, text='bad', state="*")
    dp.register_callback_query_handler(thirty_days_videos, text='every_day', state="*")
    dp.register_callback_query_handler(back_to_menu, text='back_reports', state="*")
    dp.register_callback_query_handler(back_to_video, text="back_to_video", state="*")
    dp.register_callback_query_handler(refused1_video, text="face_result", state="*")
    dp.register_callback_query_handler(refused3_video, text="send_message", state="*")
    dp.register_callback_query_handler(refused2_video, text="incorrect_code", state="*")
    dp.register_callback_query_handler(archive_button, text="archive", state="*")
    dp.register_callback_query_handler(archive_button, text="more_video", state="*")
    dp.register_callback_query_handler(back_to_menu, text="back_from_archive", state="*")
    dp.register_callback_query_handler(thirty_day_dispute, text='lets_go', state="*")
    dp.register_callback_query_handler(ninety_day_volya, text="before_result", state="*")
    dp.register_callback_query_handler(back_to_menu, text="back_from_volya", state="*")
    dp.register_callback_query_handler(new_videos_volya, text="start_volya", state="*")
    dp.register_callback_query_handler(accept_current_dispute, text='good1', state="*")
    dp.register_callback_query_handler(access_volya_dispute, text='confirm_video1', state="*")
    dp.register_callback_query_handler(refused_video_thirty_day, text="bad_video_day", state="*")
    dp.register_callback_query_handler(refused_video_thirty_day, text='bad1', state="*")
