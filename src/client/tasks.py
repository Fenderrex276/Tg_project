from datetime import datetime

from aiogram import Dispatcher
from pytz import utc

from client.initialize import scheduler, dp
from db.models import PeriodicTask


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
    return [str(int(hour) + int(t_zone)), str(minute), str(second)]


def scheduler_add_job(dp: Dispatcher, t_zone, fun: str, user_id: int, flag: int = -1):
    time = time_calculated(t_zone)
    #time[0] = '*'
    #time[1] = '*'

    if fun == "reminder":
        if flag == 1:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы остановились на внесении депозита. Может продолжим?"}

            scheduler.add_job(send_reminder, 'cron', id=f'{user_id}_reminder', hour=time[0], minute=time[1],
                              second=time[2],
                              kwargs=kwargs)
            kwargs.pop('dp')
            PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder", hour=time[0],
                                        minute=time[1], second=time[2],
                                        kwargs=kwargs)

        elif flag == 2:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"}

            scheduler.add_job(send_reminder, 'cron', hour=time[0], minute=time[1], second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder", hour=time[0],
                                        minute=time[1], second=time[2],
                                        kwargs=kwargs)
        elif flag == 3:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не завершили внесение депозита. Хотите получить реквизиты?"}

            scheduler.add_job(send_reminder, 'cron', hour=time[0], minute=time[1], second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder", hour=time[0],
                                        minute=time[1], second=time[2],
                                        kwargs=kwargs)
        elif flag == 4:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не подтвердили желание внести депозит. Хотите продолжить?"}

            scheduler.add_job(send_reminder, 'cron', hour=time[0], minute=time[1], second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder", hour=time[0],
                                        minute=time[1], second=time[2],
                                        kwargs=kwargs)
        elif flag == 5:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы внесли депозит, пора начать вашу первый этап диспута. Хотите продолжить?"}

            scheduler.add_job(send_reminder, 'cron', hour=time[0], minute=time[1], second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder", hour=time[0],
                                        minute=time[1], second=time[2],
                                        kwargs=kwargs)
        elif flag == 6:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"}

            scheduler.add_job(send_reminder, 'cron', hour=time[0], minute=time[1], second=time[2],
                              id=f'{user_id}_reminder',
                              kwargs=kwargs)
            kwargs.pop('dp')
            PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_reminder', fun="reminder", hour=time[0],
                                        minute=time[1], second=time[2],
                                        kwargs=kwargs)
        # elif flag == 7:
        #     scheduler.add_job(send_reminder, 'cron', misnute="*", id=f'{user_id}_reminder',
        #                       kwargs={"call": user_id, "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})
        # elif flag == 8:
        #     scheduler.add_job(send_reminder, 'cron', misnute="*", id=f'{user_id}_reminder',
        #                       kwargs={"call": user_id, "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})

    elif fun == "code":
        scheduler.add_job(send_code, 'cron', id=f'{user_id}_code', minute="*",
                          kwargs={"dp": dp, "user_id": user_id,
                                  "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
    elif fun == "content":
        scheduler.add_job(send_content, 'cron', id=f'{user_id}_content', minute="*",
                          kwargs={"dp": dp, "user_id": user_id,
                                  "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
        # elif fun == "":
        #     scheduler.add_job(send_content, 'cron', minute="*")


def load_periodic_tasks():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        kwargs['dp'] = dp
        # if task.fun == "reminder":
        scheduler.add_job(send_reminder, 'cron', id=f'{task.job_id}', hour=f'{task.hour}',
                          minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)
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


async def send_content():  # Скипнуть
    # Когда нужно присылать уведомления и откуда их брать
    print("Если ты это читаешь в консольке, то периодический таск работает")


async def send_code():
    # Лежит в admin/reports/callbacks
    # TODO НЕ ебу как будет лучше сделать
    pass


def del_scheduler(job_id: str):
    PeriodicTask.objects.filter(job_id=job_id).delete()
    scheduler.remove_job(job_id=job_id)
