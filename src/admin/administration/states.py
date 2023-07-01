from aiogram.dispatcher.filters.state import State, StatesGroup


class AdministrationStates(StatesGroup):
    none = State()
    input_username_admin = State()
    delete_admin = State()
    make_super_admin = State()
    remove_super_admin = State()
    move_to_dialog_with_admin = State()
    activate_admin = State()
    deactivate_admin = State()
    notify_all_administrators = State()
    notify_all_users = State()
    delete_promo = State()
    give_promo = State()
