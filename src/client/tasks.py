from aiogram import Dispatcher

from client.initialize import scheduler
from admin.reports.callbacks import new_code


def scheduler_add_job(dp: Dispatcher, fun: str, user_id: int, flag: int = -1):
    if fun == "reminder":
        if flag == 1:
            scheduler.add_job(send_reminder, 'cron', id=f'{user_id}_reminder', second="*/10",
                              kwargs={"dp": dp, "user_id": user_id,
                                      "msg": "Вы остановились на внесении депозита. Может продолжим?"})
        elif flag == 2:
            scheduler.add_job(send_reminder, 'cron', second="*/10", id=f'{user_id}_reminder',
                              kwargs={"dp": dp, "user_id": user_id,
                                      "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?"})
        elif flag == 3:
            scheduler.add_job(send_reminder, 'cron', second="*/10", id=f'{user_id}_reminder',
                              kwargs={"dp": dp, "user_id": user_id,
                                      "msg": "Вы так и не завершили внесение депозита. Хотите получить реквизиты?"})
        elif flag == 4:
            scheduler.add_job(send_reminder, 'cron', second="*/10", id=f'{user_id}_reminder',
                              kwargs={"dp": dp, "user_id": user_id,
                                      "msg": "Вы так и не подтвердили желание внести депозит. Хотите продолжить?"})
        elif flag == 5:
            scheduler.add_job(send_reminder, 'cron', second="*/10", id=f'{user_id}_reminder',
                              kwargs={"dp": dp, "user_id": user_id,
                                      "msg": "Вы внесли депозит, пора начать вашу первый этап диспута. Хотите продолжить?"})
        elif flag == 6:
            scheduler.add_job(send_reminder, 'cron', second="*/10", id=f'{user_id}_reminder',
                              kwargs={"dp": dp, "user_id": user_id,
                                      "msg": "Начните свою первую тренировку уже сейчас. Хотите продолжить?"})
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
    scheduler.remove_job(job_id=job_id)
