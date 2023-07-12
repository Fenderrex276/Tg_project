import logging

from aiogram import Bot, Dispatcher, types

from admin.administration.states import AdministrationStates
from admin.initialize import bot as bot_a
from client.initialize import bot as bot_c
from db.models import DisputeAdmin, User, BlogerPromocodes

logger = logging.getLogger(__name__)


class Administration:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        pass

    def register_handlers(self):
        self.dp.register_message_handler(self.input_username_admin, state=AdministrationStates.input_username_admin)
        self.dp.register_message_handler(self.delete_admin, state=AdministrationStates.delete_admin)
        self.dp.register_message_handler(self.make_super_admin, state=AdministrationStates.make_super_admin)
        self.dp.register_message_handler(self.remove_super_admin, state=AdministrationStates.remove_super_admin)
        self.dp.register_message_handler(self.move_to_dialog, state=AdministrationStates.move_to_dialog_with_admin)
        self.dp.register_message_handler(self.activate_admin, state=AdministrationStates.activate_admin)
        self.dp.register_message_handler(self.deactivate_admin, state=AdministrationStates.deactivate_admin)
        self.dp.register_message_handler(self.notify_all_administrators,
                                         state=AdministrationStates.notify_all_administrators)

        self.dp.register_message_handler(self.delete_promo, state=AdministrationStates.delete_promo)
        self.dp.register_message_handler(self.give_promo, state=AdministrationStates.give_promo)

        self.dp.register_message_handler(self.notify_all_users,
                                         state=AdministrationStates.notify_all_users)

    async def input_username_admin(self, message: types.Message):
        if DisputeAdmin.objects.filter(username=message['text']).exists():
            await message.answer("В системе уже есть админ с таким username.")
        else:

            DisputeAdmin.objects.create(username=message['text'])
            await AdministrationStates.none.set()
            await message.answer("Готово!")

    async def delete_admin(self, message: types.Message):

        try:
            admin = DisputeAdmin.objects.get(username=message['text'])
            admin.delete()
            await AdministrationStates.none.set()
            await message.answer("Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого админа. Введите username повторно.")

    async def make_super_admin(self, message: types.Message):

        try:
            admin = DisputeAdmin.objects.get(username=message['text'])
            admin.is_super_admin = True
            admin.save()
            await AdministrationStates.none.set()
            await message.answer("Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого админа. Введите username повторно.")

    async def remove_super_admin(self, message: types.Message):

        try:
            admin = DisputeAdmin.objects.get(username=message['text'])
            admin.is_super_admin = False
            admin.save()
            await AdministrationStates.none.set()
            await message.answer("Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого админа. Введите username повторно.")

    async def move_to_dialog(self, message: types.Message):

        try:
            DisputeAdmin.objects.get(username=message['text'])
            await AdministrationStates.none.set()
            await message.answer(
                f"Готово!\nДля перехода в диалогу нажмите на эту ссылку https://t.me/{message['text']}")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого админа. Введите username повторно.")

    async def activate_admin(self, message: types.Message):

        try:
            admin = DisputeAdmin.objects.get(username=message['text'])
            admin.is_active = True
            admin.save()
            await AdministrationStates.none.set()
            await message.answer(f"Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого админа. Введите username повторно.")

    async def deactivate_admin(self, message: types.Message):

        try:
            admin = DisputeAdmin.objects.get(username=message['text'])
            admin.is_active = False
            admin.save()
            await AdministrationStates.none.set()
            await message.answer(f"Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого админа. Введите username повторно.")

    async def notify_all_administrators(self, message: types.Message):
        admins = DisputeAdmin.objects.filter(is_active=True).exclude(user_id=message["from"]["id"])
        for admin in admins:
            await bot_a.send_message(chat_id=admin.chat_id, text=message['text'])

        await AdministrationStates.none.set()
        await message.answer(f"Готово!")

    async def notify_all_users(self, message: types.Message):
        users = User.objects.all()
        for user in users:
            await bot_c.send_message(chat_id=user.chat_id, text=message['text'])

        await AdministrationStates.none.set()
        await message.answer(f"Готово!")

    async def delete_promo(self, message: types.Message):

        try:
            promo = BlogerPromocodes.objects.get(promocode=message['text'])
            promo.delete()
            await AdministrationStates.none.set()
            await message.answer("Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого промокода. Введите код повторно.")

    async def give_promo(self, message: types.Message):

        try:
            promo = BlogerPromocodes.objects.get(promocode=message['text'])
            promo.is_issued = True
            promo.save()
            await AdministrationStates.none.set()
            await message.answer("Готово!")
        except DisputeAdmin.DoesNotExist:
            await message.answer("В системе нет такого промокода. Введите код повторно.")
