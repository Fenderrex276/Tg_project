from datetime import datetime

from aiogram import Dispatcher
from pytz import utc

from client.initialize import scheduler, dp
from db.models import PeriodicTask
from utils import get_current_timezone


def time_calculated(t_zone):
    time_now = datetime.now(tz=utc)
    hour = time_now.hour
    minute = time_now.minute
    second = time_now.second
    # print(f'Тайм зона: {t_zone}')
    # print(f'Сейчас по UTC: {time_now}')
    # print(f'Часы: {hour}')
    # print(f'Минуты: {minute}')
    # print(f'Секунды: {second}')
    if ":" not in t_zone:
        t_zone += ":00"
    print(t_zone)

    t_zone_hours, t_zone_minutes = get_current_timezone(t_zone)

    # TODO [DEPRECATED] for SIM: Мааааакс, тут надо конкретно поебаться ещё с добавлением или вычитанием
    #  таймзоны относительно UTC^ я тут хуйни наделал но надеюсь потом ты грамотно рассмотришь все ситуации
    return [str((hour + t_zone_hours) % 24), str((minute + t_zone_minutes) % 60), str(second)]


async def scheduler_add_job(dp: Dispatcher, t_zone, fun: str, user_id: int, flag: int = -1):
    time = time_calculated(t_zone)
    # time[0] = '*'
    # time[1] = '*'
    print(time)
    if fun == "reminder":  # TODO RUS Нужно добавить кнопки после уведомлений и порешать вопрос с удалением уведомления
        if flag == 1:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы остановились на внесении депозита. Может продолжим?"}

            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', id=f'{user_id}_reminder',
                              day_of_week='*', hour=time[0], minute=time[1],
                              second=time[2],
                              kwargs=kwargs)
            # TODO [DEPRECATED] for SIM: 'conflicts with an existing job'' крч тут такая ошибка вылезала,
            #  я в функцию add_job добавил параметр 'replace_existing=True' хз, вроде не смертельно но чекнуть стоит
            kwargs.pop('dp')
            await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder",
                                               day_of_week='*',
                                               hour=time[0],
                                               minute=time[1], second=time[2],
                                               kwargs=kwargs)

        elif flag == 2:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"}

            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', day_of_week='*', hour=time[0],
                              minute=time[1],
                              second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder",
                                               day_of_week='*',
                                               hour=time[0],
                                               minute=time[1], second=time[2],
                                               kwargs=kwargs)
        elif flag == 3:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не завершили внесение депозита. Хотите получить реквизиты?"}

            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', day_of_week='*', hour=time[0],
                              minute=time[1],
                              second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder",
                                               day_of_week='*',
                                               hour=time[0],
                                               minute=time[1], second=time[2],
                                               kwargs=kwargs)
        elif flag == 4:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не подтвердили желание внести депозит. Хотите продолжить?"}

            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', day_of_week='*', hour=time[0],
                              minute=time[1],
                              second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder",
                                               day_of_week='*',
                                               hour=time[0],
                                               minute=time[1], second=time[2],
                                               kwargs=kwargs)
        elif flag == 5:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы внесли депозит, пора начать вашу первый этап диспута. Хотите продолжить?"}

            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', day_of_week='*', hour=time[0],
                              minute=time[1],
                              second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder",
                                               day_of_week='*',
                                               hour=time[0],
                                               minute=time[1], second=time[2],
                                               kwargs=kwargs)
        elif flag == 6:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"}

            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', day_of_week='*', hour=time[0],
                              minute=time[1],
                              second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder",
                                               day_of_week='*',
                                               hour=time[0],
                                               minute=time[1], second=time[2],
                                               kwargs=kwargs)
        # elif flag == 7:
        #     scheduler.add_job(send_reminder, 'cron', misnute="*", id=f'{user_id}_reminder',
        #                       kwargs={"call": user_id, "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})
        # elif flag == 8:
        #     scheduler.add_job(send_reminder, 'cron', misnute="*", id=f'{user_id}_reminder',
        #                       kwargs={"call": user_id, "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})

    elif fun == "code":
        scheduler.add_job(send_code, replace_existing=True, trigger='cron', id=f'{user_id}_code', minute="*",
                          kwargs={"dp": dp, "user_id": user_id,
                                  "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
    elif fun == "content":
        scheduler.add_job(send_content, replace_existing=True, trigger='cron', id=f'{user_id}_content', minute="*",
                          kwargs={"dp": dp, "user_id": user_id,
                                  "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
        # elif fun == "":
        #     scheduler.add_job(send_content, 'cron', minute="*")


async def init_send_code(user_id, chat_id, when, id_video):
    from datetime import date
    from settings.settings import TEST
    my_date = date.today()
    if TEST:
        print("Was init")
        time_now = datetime.now(tz=utc)
        hour = time_now.hour
        minute = time_now.minute
        second = time_now.second
        week_day = '*'  # my_date.weekday()

        scheduler.add_job(send_first_code, replace_existing=True, trigger='cron', day_of_week=str(week_day),
                          hour='*',
                          minute='*/5',
                          id=f'{user_id}_send_first_code',
                          kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})
        # kwargs.pop('dp')
        await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_send_first_code', fun="send_first_code",
                                           day_of_week=str(week_day), hour='*',
                                           minute='*/5',
                                           kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})
        print(scheduler.print_jobs())
    elif when == "послезавтра":
        print("Was послезавтра")
        week_day = '*'  # (my_date.weekday() + 2) % 7
        scheduler.add_job(send_first_code, replace_existing=True, trigger='cron', day_of_week=str(week_day), hour='*',
                          minute='*/5',
                          id=f'{user_id}_send_first_code',
                          kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})
        # kwargs.pop('dp')
        await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_send_first_code', fun="send_first_code",
                                           day_of_week=str(week_day), hour='*',
                                           minute='*/5',
                                           kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})
    # elif flag == 7:
    else:
        print("Was Понедельник")

        week_day = '*'
        scheduler.add_job(send_first_code, replace_existing=True, trigger='cron', day_of_week=str(week_day), hour='*',
                          minute='*/5',
                          id=f'{user_id}_send_first_code',
                          kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})
        # kwargs.pop('dp')
        await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_send_first_code', fun="send_first_code",
                                           day_of_week=str(week_day), hour='*',
                                           minute='*/5',
                                           kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})


# TODO Адаптировать под новые переодические функции
def load_periodic_tasks():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        kwargs['dp'] = dp
        if task.fun == "reminder":
            scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', id=f'{task.job_id}',
                              day_of_week=f'{task.day_of_week}',
                              hour=f'{task.hour}',
                              minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)
        elif task.fun == "send_code":
            print('Task send_code')
            scheduler.add_job(send_code, replace_existing=True, trigger='cron', day_of_week=str(task.day_of_week),
                              hour='*',
                              minute='*/5',
                              id=f'{kwargs["user_id"]}_send_code',
                              kwargs={'user_id': kwargs['user_id'], 'chat_id': kwargs['chat_id'],
                                      'id_video': kwargs['id_video']})
        elif task.fun == "send_first_code":
            print('Task send_first_code')
            scheduler.add_job(send_first_code, replace_existing=True, trigger='cron', day_of_week=str(task.day_of_week),
                              hour='*',
                              minute='*/5',
                              id=f'{kwargs["user_id"]}_send_first_code',
                              kwargs={'user_id': kwargs['user_id'], 'chat_id': kwargs['chat_id'],
                                      'id_video': kwargs['id_video']})
        print(scheduler.print_jobs())
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
    print("Was FIRST_SEND")
    from admin.reports.callbacks import new_code
    await new_code(chat_id, user_id, id_video)
    del_scheduler(f'{user_id}_send_first_code')
    week_day = '*'
    scheduler.add_job(send_code, replace_existing=True, trigger='cron', day_of_week=str(week_day), hour='*',
                      minute='*/5',
                      second='0',
                      id=f'{user_id}_send_code',
                      kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})

    await PeriodicTask.objects.acreate(user_id=user_id, job_id=f'{user_id}_send_code', fun="send_code",
                                       day_of_week=str(week_day), hour='*',
                                       minute='*/5',
                                       second='0',
                                       kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})


async def send_content():  # Скипнуть
    # Когда нужно присылать уведомления и откуда их брать
    print("Если ты это читаешь в консольке, то периодический таск работает")


async def send_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code
    await new_code(chat_id, user_id, id_video)


def del_scheduler(job_id: str):
    PeriodicTask.objects.filter(job_id=job_id).delete()
    scheduler.remove_job(job_id=job_id)
