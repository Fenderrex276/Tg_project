import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from admin.administration.keyboards import actions_with_admins
from admin.administration.states import AdministrationStates

from db.models import DisputeAdmin

logger = logging.getLogger(__name__)


async def show_admins(call: types.CallbackQuery, state: FSMContext):
    await AdministrationStates.none.set()
    admins_keyboard = types.InlineKeyboardMarkup()
    admins_keyboard.add(types.InlineKeyboardButton(text=f"Добавить администратора", callback_data="add_admins"))
    admins = DisputeAdmin.objects.all()
    for admin in admins:
        admins_keyboard.add(
            types.InlineKeyboardButton(
                text=f"{admin.username} | {'Активен' if admin.is_active else 'Неактивен'} | {'Супер Админ' if admin.is_super_admin else 'Простой Админ'}",
                callback_data=f"action_with_admin : {admin.username}"))
    await call.message.answer(text="Список администраторов", reply_markup=admins_keyboard)


async def add_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName добавляемого администратора."
    await AdministrationStates.input_username_admin.set()
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_input_admin")
    ))
    await call.answer()


async def delete_admin(call: types.CallbackQuery, state: FSMContext):
    tmp_msg = "Введи UserName удаляемого администратора."
    await AdministrationStates.delete_admin.set()
    await call.message.edit_text(text=tmp_msg, reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Назад', callback_data="back_from_input_admin")
    ))
    await call.answer()


def register_callback(dp: Dispatcher, bot):
    # @dp.callback_query_handler(filters.Regexp(regexp='^ban data.+'))

    dp.register_callback_query_handler(show_admins, text='admins', state='*')
    dp.register_callback_query_handler(add_admin, text='add_admins', state='*')
    dp.register_callback_query_handler(show_admins, text='back_from_input_admin', state='*')
    # dp.register_callback_query_handler(action_admin, text=filters.Regexp(regexp='^action_with_admin : '), state='*')
