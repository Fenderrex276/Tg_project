from datetime import date
from datetime import datetime

from aiogram import Dispatcher
from pytz import utc

from admin.initialize import scheduler as admin_scheduler
from client.initialize import scheduler as client_scheduler, dp
from db.models import PeriodicTask
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


# TODO Добавить возможность периодичного вызова
async def reminder_scheduler_add_job(dp: Dispatcher, t_zone: str, fun: str, user_id: int, flag: int = -1,
                                     notification_hour=None,
                                     notification_min=None):
    hour, minute, second = time_calculated(t_zone, notification_hour, notification_min)

    if fun == "reminder":  # TODO RUS Нужно добавить кнопки после уведомлений и порешать вопрос с удалением уведомления
        if flag == 1:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы остановились на внесении депозита. Может продолжим?"}

        elif flag == 2:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"}

        elif flag == 3:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не завершили внесение депозита. Хотите получить реквизиты?"}

        elif flag == 4:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не подтвердили желание внести депозит. Хотите продолжить?"}

        elif flag == 5:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы внесли депозит, пора начать вашу первый этап диспута. Хотите продолжить?"}

        elif flag == 6:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"}
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

        # elif flag == 7:
        #     scheduler.add_job(send_reminder, 'cron', misnute="*", id=f'{user_id}_reminder',
        #                       kwargs={"call": user_id, "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})
        # elif flag == 8:
        #     scheduler.add_job(send_reminder, 'cron', misnute="*", id=f'{user_id}_reminder',
        #                       kwargs={"call": user_id, "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})

    # elif fun == "code":
    #     scheduler.add_job(send_code, replace_existing=True, trigger='cron', id=f'{user_id}_code', minute="*",
    #                       kwargs={"dp": dp, "user_id": user_id,
    #                               "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
    # elif fun == "content":
    #     scheduler.add_job(send_content, replace_existing=True, trigger='cron', id=f'{user_id}_content', minute="*",
    #                       kwargs={"dp": dp, "user_id": user_id,
    #                               "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
    # elif fun == "":
    #     scheduler.add_job(send_content, 'cron', minute="*")


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
        day_of_week = (my_date.weekday() + 2) % 7
    else:
        print("Was Понедельник")
        day_of_week = '0'

    kwargs = {'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video}
    add_job(admin_scheduler, call_fun=send_first_code, str_name='send_first_code', user_id=user_id,
            day_of_week=str(day_of_week),
            hour=hour,
            minute=minute, second=second, kwargs=kwargs)

    admin_scheduler.print_jobs()


# TODO Адаптировать под новые периодические функции
def load_periodic_tasks():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        if task.fun == "reminder":

            kwargs['dp'] = dp
            client_scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', id=f'{task.job_id}',
                                     day_of_week=task.day_of_week,
                                     hour=f'{task.hour}',
                                     minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)
        elif task.fun == "send_code":
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
        print(f'CLIENT_SCHEDULER\n{client_scheduler.print_jobs()}')
        print(f'ADMIN_SCHEDULER\n{admin_scheduler.print_jobs()}')
        # elif task.fun == "code":
        #     scheduler.add_job(send_code, 'cron', id=f'{task.job_id}', hour=f'{task.hour}',
        #                       minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)
        # elif task.fun == "content":
        #     scheduler.add_job(send_content(), 'cron', id=f'{task.job_id}', hour=f'{task.hour}',
        #                       minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)


async def send_reminder(dp: Dispatcher, user_id: int, msg: str):
    await dp.bot.send_message(user_id, msg)
    # TODO Добавляем кнопку "Продолжить"
    # TODO Новые состояния


async def send_first_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code
    print("Was FIRST_SEND")

    await new_code(chat_id, user_id, id_video)
    scheduler = PeriodicTask.objects.get(job_id=f'{user_id}_send_first_code')
    del_scheduler(f'{user_id}_send_first_code', 'admin')
    add_job(admin_scheduler, call_fun=send_code, str_name='send_code', user_id=user_id,
            day_of_week=scheduler.day_of_week,
            hour=scheduler.hour,
            minute=scheduler.minute,
            second=scheduler.second, kwargs=scheduler.kwargs)

    print(f'ADMIN_SCHEDULER\n{admin_scheduler.print_jobs()}')


async def send_content():  # Скипнуть
    # Когда нужно присылать уведомления и откуда их брать
    print("Если ты это читаешь в консольке, то периодический таск работает")


async def send_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code
    await new_code(chat_id, user_id, id_video)


def del_scheduler(job_id: str, where: str):
    PeriodicTask.objects.filter(job_id=job_id).delete()
    if where == 'client':
        client_scheduler.remove_job(job_id=job_id)
    elif where == 'admin':
        admin_scheduler.remove_job(job_id=job_id)
    else:
        print(f'ERROR: Неверный параметр where')
