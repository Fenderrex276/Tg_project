from datetime import date
from datetime import datetime

from aiogram import Dispatcher, types
from pytz import utc

from admin.initialize import scheduler as admin_scheduler
from client.initialize import scheduler as client_scheduler, dp
from db.models import PeriodicTask, RoundVideo, User
from settings.settings import TEST
from utils import get_current_timezone


def time_calculated(t_zone: str, notification_hour: int = None, notification_min: int = None):
    '''
    Функция возвращает время, в которое нужно присылать уведомления
    notification_hour и notification_min задают конкретное время
    Если не указывать данные параметры то вернется время по TZ UTC когда было вызвано действия
    '''
    time_now = datetime.now(tz=utc)

    second = time_now.second
    if ":" not in t_zone:
        t_zone += ":00"
    print(t_zone)
    if not notification_hour is None and not notification_min is None:
        if notification_hour >= 24 or notification_min >= 60:
            print("Неправильный формат времени")
            return
        t_zone_hours, t_zone_minutes = get_current_timezone(t_zone)
        hour = notification_hour
        minute = notification_min
        second = 0
        current_hour = str((hour + t_zone_hours) % 24)
        current_min = str((minute + t_zone_minutes) % 60)
        return [current_hour, current_min, str(second)]
    else:
        hour = time_now.hour
        minute = time_now.minute
        return [str(hour), str(minute), str(second)]


def add_job(scheduler, call_fun, str_name: str, user_id, day_of_week: str, hour: str, minute: str, second: str, kwargs):
    scheduler.add_job(call_fun, replace_existing=True, trigger='cron', id=f'{user_id}_{str_name}',
                      day_of_week=day_of_week, hour=hour, minute=minute,
                      second=second,
                      kwargs=kwargs)
    if str_name == "reminder":
        kwargs.pop('dp')
    PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_{str_name}', fun=str_name,
                                day_of_week=day_of_week,
                                hour=hour,
                                minute=minute, second=second,
                                kwargs=kwargs)


#
# def admin_add_job(call_fun, str_name: str, user_id, day_of_week: str, hour: str, minute: str, second: str, kwargs):
#     admin_scheduler.add_job(call_fun, replace_existing=True, trigger='cron', id=f'{user_id}_{str_name}',
#                             day_of_week=day_of_week, hour=hour, minute=minute,
#                             second=second,
#                             kwargs=kwargs)
#     if str_name == "reminder":
#         kwargs.pop('dp')
#     PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_{str_name}', fun=str_name,
#                                 day_of_week=day_of_week,
#                                 hour=hour,
#                                 minute=minute, second=second,
#                                 kwargs=kwargs)


# SIMA TODO Добавить возможность периодичного вызова
async def reminder_scheduler_add_job(dp: Dispatcher, t_zone: str, fun: str, user_id: int, flag: int = -1,
                                     notification_hour=None,
                                     notification_min=None):
    hour, minute, second = time_calculated(t_zone, notification_hour, notification_min)

    if fun == "reminder":  # RUS TODO  Нужно добавить кнопки после уведомлений и порешать вопрос с удалением уведомления
        if flag == 1:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы остановились на внесении депозита. Может продолжим?",
                      "callback_data": "start_pay_state"}

        elif flag == 2:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?",
                      "callback_data": "choose_current_sum"}

        elif flag == 3:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не завершили внесение депозита. Хотите получить реквизиты?",
                      "callback_data": "get_pay_details"}

        elif flag == 4:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не подтвердили желание внести депозит. Хотите продолжить?",
                      "callback_data": "confirm_deposit"}

        elif flag == 5:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы внесли депозит, пора начать вашу первый этап диспута. Хотите продолжить?",
                      "callback_data": "start_current_dispute"}

        elif flag == 6:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?",
                      "callback_data": "lets_start_training"}
        else:
            print(f'Ошибка вызова функции reminder_scheduler_add_job для создания напоминаний. Неверный flag')
            return
        if TEST:
            add_job(client_scheduler, call_fun=send_reminder, str_name='reminder', user_id=user_id, day_of_week='*',
                    hour='*',
                    minute='*/2', second='0', kwargs=kwargs)
        else:
            add_job(client_scheduler, call_fun=send_reminder, str_name='reminder', user_id=user_id, day_of_week='*',
                    hour=hour,
                    minute=minute, second=second, kwargs=kwargs)


def date_calculated(notification_hour, utc_hour, date):
    if notification_hour < utc_hour:
        date -= 1
    if date == -1:
        date = 6

    return date


async def init_send_code(user_id, chat_id, when: str, id_video: int, t_zone: str, notification_hour: int = None,
                         notification_min: int = None):
    hour, minute, second = time_calculated(t_zone, notification_hour, notification_min)
    if TEST:
        print("Was init")
        hour, minute, second = time_calculated(t_zone)
        minute = int(minute) + 5
        if minute >= 60:
            hour = str(int(hour) + 1)
            minute %= 60
        minute = str(minute)
        day_of_week = '*'
    elif when == "послезавтра":
        print("Was послезавтра")
        my_date = date.today()
        day_of_week = date_calculated(notification_hour, hour, (my_date.weekday() + 2) % 7)

    else:
        print("Was Понедельник")
        day_of_week = date_calculated(notification_hour, hour, 0)

    kwargs = {'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video}
    add_job(admin_scheduler, call_fun=send_first_code, str_name='send_first_code', user_id=user_id,
            day_of_week=str(day_of_week),
            hour=hour,
            minute=minute, second=second, kwargs=kwargs)

    admin_scheduler.print_jobs()


# SIMA TODO Адаптировать под новые периодические функции
def load_periodic_task_for_admin():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        if task.fun == "send_code":
            print('Task send_code')
            admin_scheduler.add_job(send_code, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "send_first_code":
            print('Task send_first_code')
            admin_scheduler.add_job(send_first_code, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        # print(f'ADMIN_SCHEDULER\n{admin_scheduler.print_jobs()}')
        print('-------------------------------------')
        print(f'ADMIN_GET_JOBS\n{admin_scheduler.get_job(job_id="254wdwd173575_send_first_code")}')
        print('-------------------------------------\n')
        print('-------------------------------------')
        print(f'ADMIN_PRINT_JOBS\n{admin_scheduler.print_jobs()}')
        print('-------------------------------------')


def load_periodic_task_for_client():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        if task.fun == "reminder":
            kwargs['dp'] = dp
            client_scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', id=f'{task.job_id}',
                                     day_of_week=task.day_of_week,
                                     hour=f'{task.hour}',
                                     minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)

        print(f'CLIENT_SCHEDULER\n{client_scheduler.print_jobs()}')


async def send_reminder(dp: Dispatcher, user_id: int, msg: str, callback_data: str):
    continue_keyboard = types.InlineKeyboardMarkup()
    continue_keyboard.add(types.InlineKeyboardButton(text="Продолжить", callback_data=callback_data))
    await dp.bot.send_message(user_id, msg, reply_markup=continue_keyboard)
    # RUS TODO Добавляем кнопку "Продолжить"
    # RUS TODO Новые состояния


async def send_first_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code
    print("Was FIRST_SEND")

    await new_code(chat_id, user_id, id_video)
    # scheduler = PeriodicTask.objects.get(job_id=f'{user_id}_send_first_code')
    del_scheduler(f'{user_id}_send_first_code', 'admin')
    add_job(admin_scheduler, call_fun=send_code, str_name='send_code', user_id=user_id,
            day_of_week='*',
            hour='4',
            minute='30',
            second='0', kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})

    add_soft_deadline(user_id)
    print(f'ADMIN_SCHEDULER\n{admin_scheduler.print_jobs()}')


def add_soft_deadline(user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
    if user.action == 'morning':
        if user.additional_action == 'five_am':
            hour, minute, second = time_calculated(user.timezone, 5, 0)
        elif user.additional_action == 'six_am':
            hour, minute, second = time_calculated(user.timezone, 6, 0)
        elif user.additional_action == 'seven_am':
            hour, minute, second = time_calculated(user.timezone, 7, 0)
        elif user.additional_action == 'eight_am':
            hour, minute, second = time_calculated(user.timezone, 8, 0)
        else:
            return f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}'
    else:
        hour, minute, second = time_calculated(user.timezone, 22, 0)
    add_job(admin_scheduler, call_fun=soft_deadline_reminder, str_name='soft_deadline_reminder', user_id=user_id,
            day_of_week='*',
            hour=hour,
            minute=minute,
            second=second, kwargs={'user_id': user_id})


def soft_deadline_reminder(user_id):
    instance = RoundVideo.objects.filter(user_tg_id=user_id).last()
    if instance is None:
        return f'Ошибка: Отсутствует запись для пользователя с id {user_id}'
    if instance.tg_id is None:
        # НЕ отправил
        # отправить пользователю сообщение с напоминанием
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
        dp.bot.send_message(user_id, f'{user.user_name}, ты всё ещё можешь отправить репорт')

        # создать задачу на проверку в жёсткий дедлайн и передать туда id записи RoundVideo
        del_scheduler(job_id=f'{user_id}_soft_deadline_reminder', where='admin')
        add_hard_deadline(user_id, kwargs={'user_id': user_id, 'id_round_video': instance.id})

    else:
        del_scheduler(job_id=f'{user_id}_soft_deadline_reminder', where='admin')


def add_hard_deadline(user_id, kwargs):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
    if user.action == 'morning':
        if user.additional_action == 'five_am':
            hour, minute, second = time_calculated(user.timezone, 5, 30)
            time = '5:30'
        elif user.additional_action == 'six_am':
            hour, minute, second = time_calculated(user.timezone, 6, 30)
            time = '6:30'
        elif user.additional_action == 'seven_am':
            hour, minute, second = time_calculated(user.timezone, 7, 30)
            time = '7:30'
        elif user.additional_action == 'eight_am':
            hour, minute, second = time_calculated(user.timezone, 8, 30)
            time = '8:30'
        else:
            return f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}'
    else:
        hour, minute, second = time_calculated(user.timezone, 22, 30)
        time = '22:30'
    kwargs['time'] = time
    add_job(admin_scheduler, call_fun=hard_deadline_reminder, str_name='hard_deadline_reminder', user_id=user_id,
            day_of_week='*',
            hour=hour,
            minute=minute,
            second=second, kwargs=kwargs)


def hard_deadline_reminder(user_id, id_round_video, time):
    # Говорим пользователю, что он даун
    try:
        video = RoundVideo.objects.get(id=id_round_video)
    except RoundVideo.DoesNotExist:
        return f'Ошибка: Из бд была удалена запись с id {id_round_video} для пользователя {user_id}'

    if video.tg_id is None:
        dp.bot.send_message(user_id,
                            f'Время для отправки репорта истекло. По правилам Диспута, мы ждём твой репорт каждый день до {time}')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
        if user.count_mistakes - 1 <= 0:
            # TODO RUS Прикуртить картинку
            del_scheduler(job_id=f'{user_id}_send_code', where='admin')
        user.count_mistakes -= 1
        user.save()
        del_scheduler(job_id=f'{user_id}_hard_deadline_reminder', where='admin')
    else:
        del_scheduler(job_id=f'{user_id}_hard_deadline_reminder', where='admin')


async def send_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code
    await new_code(chat_id, user_id, id_video)
    add_soft_deadline(user_id)


def del_scheduler(job_id: str, where: str):
    PeriodicTask.objects.filter(job_id=job_id).delete()
    if where == 'client':
        client_scheduler.remove_job(job_id=job_id)
    elif where == 'admin':
        admin_scheduler.remove_job(job_id=job_id)

    else:
        print(f'ERROR: Неверный параметр where')


async def change_periodic_tasks(user_id, time_zone):
    print(f"CHANGE_PERIODIC_TASK TZ: {time_zone}")
    admin_scheduler.print_jobs()
    print(f'JOBS {admin_scheduler.get_jobs()}')
    print(f'INFO {admin_scheduler.get_job(job_id=f"{user_id}_send_first_code")}')
    if admin_scheduler.get_job(job_id=f'{user_id}_send_first_code'):
        print(f"_send_first_code")
        hour, minute, second = time_calculated(time_zone, 4, 30)
        admin_scheduler.reschedule_job(f'{user_id}_send_first_code', trigger='cron', hour=hour, minute=minute,
                                       second=second)
        task = PeriodicTask.objects.get(job_id=f'{user_id}_send_first_code')
        task.hour = hour
        task.minute = minute
        task.second = second
        task.save()

    if admin_scheduler.get_job(job_id=f'{user_id}_send_code'):
        hour, minute, second = time_calculated(time_zone, 4, 30)
        admin_scheduler.reschedule_job(f'{user_id}_send_code', trigger='cron', hour=hour, minute=minute,
                                       second=second)
    if admin_scheduler.get_job(job_id=f'{user_id}_soft_deadline_reminder'):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
        if user.action == 'morning':
            if user.additional_action == 'five_am':
                hour, minute, second = time_calculated(user.timezone, 5, 0)
            elif user.additional_action == 'six_am':
                hour, minute, second = time_calculated(user.timezone, 6, 0)
            elif user.additional_action == 'seven_am':
                hour, minute, second = time_calculated(user.timezone, 7, 0)
            elif user.additional_action == 'eight_am':
                hour, minute, second = time_calculated(user.timezone, 8, 0)
            else:
                return f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}'
            admin_scheduler.reschedule_job(f'{user_id}_soft_deadline_reminder', trigger='cron', hour=hour,
                                           minute=minute,
                                           second=second)
        else:
            hour, minute, second = time_calculated(user.timezone, 22, 0)
            admin_scheduler.reschedule_job(f'{user_id}_soft_deadline_reminder', trigger='cron', hour=hour,
                                           minute=minute,
                                           second=second)
    if admin_scheduler.get_job(job_id=f'{user_id}_hard_deadline_reminder'):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
        if user.action == 'morning':
            if user.additional_action == 'five_am':
                hour, minute, second = time_calculated(user.timezone, 5, 30)

            elif user.additional_action == 'six_am':
                hour, minute, second = time_calculated(user.timezone, 6, 30)

            elif user.additional_action == 'seven_am':
                hour, minute, second = time_calculated(user.timezone, 7, 30)

            elif user.additional_action == 'eight_am':
                hour, minute, second = time_calculated(user.timezone, 8, 30)

            else:
                return f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}'
            admin_scheduler.reschedule_job(f'{user_id}_hard_deadline_reminder', trigger='cron', hour=hour,
                                           minute=minute,
                                           second=second)
        else:
            hour, minute, second = time_calculated(user.timezone, 22, 30)
            admin_scheduler.reschedule_job(f'{user_id}_hard_deadline_reminder', trigger='cron', hour=hour,
                                           minute=minute,
                                           second=second)
    if client_scheduler.get_job(job_id=f'{user_id}_reminder'):
        hour, minute, second = time_calculated(time_zone, 10, 0)
        client_scheduler.reschedule_job(f'{user_id}_reminder', trigger='cron', hour=hour, minute=minute,
                                        second=second)
    # TODO Менять уведомления с полезным материалом когда сделаю
