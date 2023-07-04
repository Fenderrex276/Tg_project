import logging
import secrets

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from admin.administration.states import AdministrationStates
from admin.initialize import storage
from db.models import DisputeAdmin, BlogerPromocodes, PeriodicTask

logger = logging.getLogger(__name__)


async def show_admins(call: types.CallbackQuery, state: FSMContext):
    await AdministrationStates.none.set()
    admins_keyboard = types.InlineKeyboardMarkup()
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Добавить администратора", callback_data="add_admin"))
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Удалить администратора", callback_data="delete_admin"))
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Сделать супер-админом", callback_data="make_super_admin"))
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Отнять супер-админа", callback_data="remove_super_admin"))
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Активировать админа", callback_data="activate_admin"))
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Деактивировать админа", callback_data="deactivate_admin"))
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Перейти в диалог", callback_data="move_to_dialog"))
    admins = DisputeAdmin.objects.all()
    msg = "Список администраторов\n\n"
    for admin in admins:
        msg += f"{admin.username}\t|\t{'Активен' if admin.is_active else 'Неактивен'}\t|\t{'Супер Админ' if admin.is_super_admin else 'Простой Админ'}\n\n"
    await call.message.answer(text="Список администраторов", reply_markup=admins_keyboard)


async def add_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName добавляемого администратора."
    await AdministrationStates.input_username_admin.set()
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def delete_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName удаляемого администратора."
    await AdministrationStates.delete_admin.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def make_super_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName для предоставления прав супер-администратора."
    await AdministrationStates.make_super_admin.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def remove_super_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName для отмены прав супер-администратора."
    await AdministrationStates.remove_super_admin.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def move_to_dialog(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName администратора, чтобы получить ссылку на чат."
    await AdministrationStates.move_to_dialog_with_admin.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def activate_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName администратора, чтобы сделать его неактивным."
    await AdministrationStates.activate_admin.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def deactivate_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName администратора, чтобы сделать его неактивным."
    await AdministrationStates.deactivate_admin.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def notify_all_administrators(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи сообщение для активных администраторов."
    await AdministrationStates.notify_all_administrators.set()
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def notify_all_users(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи сообщение для пользователей."
    await AdministrationStates.notify_all_users.set()
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_admin")
    ))
    await call.answer()


async def promocod_actions(call: types.CallbackQuery, state: FSMContext):
    await AdministrationStates.none.set()
    promo_keyboard = types.InlineKeyboardMarkup()
    promo_keyboard.add(types.InlineKeyboardButton(text=f"Добавить промокод", callback_data="add_promo"))
    promo_keyboard.add(types.InlineKeyboardButton(text=f"Удалить промокод", callback_data="delete_promo"))
    promo_keyboard.add(types.InlineKeyboardButton(text=f"Выдать промокод", callback_data="give_promo"))
    promo_keyboard.add(types.InlineKeyboardButton(text=f"Список промокодов", callback_data="list_promo"))

    await call.message.answer(text="Список действий", reply_markup=promo_keyboard)


async def add_promo(call: types.CallbackQuery, state: FSMContext):
    promo = secrets.token_hex(nbytes=5)
    BlogerPromocodes.objects.create(promocode=promo)
    tmp_msg = f"Сгенерирован промокод:\n{promo}"
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_promo")
    ))
    await call.answer()


async def delete_promo(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи промокод для удаления."
    await AdministrationStates.delete_promo.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_promo")
    ))
    await call.answer()


async def give_promo(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи промокод, который хотите выдать."
    await AdministrationStates.give_promo.set()
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_promo")
    ))
    await call.answer()


async def list_promo(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Список промокодов\n\n"
    promos = BlogerPromocodes.objects.all()
    for promo in promos:
        tmp_msg += f"{promo.promocode}\t|\t{'Выдан' if promo.is_issued else 'Свободен'}\n"
    await call.message.answer(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_action_promo")
    ))


async def statistic(call: types.CallbackQuery, state: FSMContext):
    tasks = PeriodicTask.objects.all()  # .values_list("user_id", flat=True).distinct()
    out_game = 0
    in_game = 0
    in_test_game = 0
    out_test_game = 0
    for task in tasks:
        if task.fun == "send_reminder_after_end":
            out_game += 1
        elif task.fun in ["send_code", "send_first_code"]:
            in_game += 1
        elif task.fun == "send_test_period_reminder":
            in_test_game += 1
        elif task.fun == "reminder":
            out_test_game += 1

    msg = f"""
        [Статистика по боту]\n\n
        Окончили диспут: {out_game}\n\n
        В игре: {in_game}\n\n
        На этапе подготовки: {in_test_game}\n\n
        Выбирают диспут: {out_test_game}"""

    await call.message.answer(text=msg)


def register_callback(dp: Dispatcher, bot):
    dp.register_callback_query_handler(show_admins, text='admins', state='*')
    dp.register_callback_query_handler(add_admin, text='add_admin', state='*')
    dp.register_callback_query_handler(delete_admin, text='delete_admin', state='*')
    dp.register_callback_query_handler(make_super_admin, text='make_super_admin', state='*')
    dp.register_callback_query_handler(remove_super_admin, text='remove_super_admin', state='*')
    dp.register_callback_query_handler(move_to_dialog, text='move_to_dialog', state='*')
    dp.register_callback_query_handler(activate_admin, text='activate_admin', state='*')
    dp.register_callback_query_handler(deactivate_admin, text='deactivate_admin', state='*')
    dp.register_callback_query_handler(notify_all_administrators, text='notification_admins', state='*')
    dp.register_callback_query_handler(notify_all_users, text='notification_users', state='*')
    dp.register_callback_query_handler(show_admins, text='back_from_action_admin', state='*')

    dp.register_callback_query_handler(promocod_actions, text='promo_codes', state='*')
    dp.register_callback_query_handler(promocod_actions, text='back_from_action_promo', state='*')
    dp.register_callback_query_handler(add_promo, text='add_promo', state='*')
    dp.register_callback_query_handler(delete_promo, text='delete_promo', state='*')
    dp.register_callback_query_handler(give_promo, text='give_promo', state='*')
    dp.register_callback_query_handler(list_promo, text='list_promo', state='*')
    dp.register_callback_query_handler(statistic, text='statistic', state='*')
