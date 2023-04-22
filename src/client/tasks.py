import logging
from datetime import date
from datetime import datetime

from aiogram import Dispatcher, types
from pytz import utc

from admin.initialize import scheduler as admin_scheduler
from client.initialize import scheduler as client_scheduler, dp
from db.models import PeriodicTask, RoundVideo, User
from settings.settings import TEST
from utils import get_current_timezone

logger = logging.getLogger(__name__)


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

    if str_name in ["reminder", "send_test_period_reminder", "send_reminder_after_end"]:
        kwargs.pop('dp')
    PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_{str_name}', fun=str_name,
                                day_of_week=day_of_week,
                                hour=hour,
                                minute=minute, second=second,
                                kwargs=kwargs)
    logger.info(f"ADD_JOB: Добавили задачу {str_name} для пользователя с id: {user_id}")


async def reminder_scheduler_add_job(dp: Dispatcher, t_zone: str, fun: str, user_id: int, flag: int = -1,
                                     notification_hour=None,
                                     notification_min=None):
    hour, minute, second = time_calculated(t_zone, notification_hour, notification_min)
    PeriodicTask.objects.filter(job_id=f"{user_id}_send_reminder_after_end").delete()
    del_scheduler(job_id=f"{user_id}_send_reminder_after_end", where='client')
    if fun == "reminder":  # TODO RUS Проверить какую-то кнопку на удаление, я чекнул, первые четыре кнопки робят
        # TODO Надо поглядеть чтобы пользователь не мог сменить игру иначе порешать с уведомлениями
        if flag == 1:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы остановились на внесении депозита. Может продолжим?",
                      "callback_data": "start_pay_state", "count": 0}

        elif flag == 2:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не выбрали сумму депозита. Хотите продолжить?",
                      "callback_data": "choose_current_sum", "count": 0}

        elif flag == 3:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не завершили внесение депозита. Хотите получить реквизиты?",
                      "callback_data": "get_pay_details", "count": 0}

        elif flag == 4:
            kwargs = {"dp": dp, "user_id": user_id,
                      "msg": "Вы так и не подтвердили желание внести депозит. Хотите продолжить?",
                      "callback_data": "confirm_deposit", "count": 0}
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
    # TODO RUS  Нужно добавить кнопки после уведомлений и порешать вопрос с удалением уведомления. Добавить callback_data
    elif fun == "send_test_period_reminder":
        kwargs = {"dp": dp, "user_id": user_id,
                  "msg": "⚠ Осталось 6 день, чтобы завершить подготовку к цели. Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6 дней, иначе на 7 день спор будет проигран.",
                  "count": 1}
        add_job(client_scheduler, call_fun=send_test_period_reminder, str_name='send_test_period_reminder',
                user_id=user_id, day_of_week='*',
                hour=hour,
                minute=minute, second=second, kwargs=kwargs)
    elif fun == "send_reminder_after_end":
        kwargs = {"dp": dp, "user_id": user_id,
                  "msg": "Бросьте себе вызов! Проверьте себя на прочность!", "count": 0}
        add_job(client_scheduler, call_fun=send_reminder_after_end, str_name='send_reminder_after_end',
                user_id=user_id, day_of_week='*',
                hour=hour,
                minute=minute, second=second, kwargs=kwargs)


async def send_reminder(dp: Dispatcher, user_id: int, msg: str, callback_data: str, count: int = 0):
    continue_keyboard = types.InlineKeyboardMarkup()
    continue_keyboard.add(types.InlineKeyboardButton(text="Продолжить", callback_data=callback_data))

    try:
        task = PeriodicTask.objects.get(job_id=f"{user_id}_reminder")
    except PeriodicTask.DoesNotExist:
        logger.critical(f"SEND_REMINDER: Ошибка! Периодической задачи с id {user_id}_reminder не существует")
        return f'SEND_REMINDER: Ошибка! Периодической задачи с id {user_id}_reminder не существует'

    task.kwargs['count'] = count + 1
    kwargs = task.kwargs
    kwargs['dp'] = dp
    client_scheduler.modify_job(job_id=f"{user_id}_reminder", kwargs=kwargs)
    my_date = date.today()
    if count == 0:

        weak = my_date.weekday()
        client_scheduler.reschedule_job(job_id=f"{user_id}_reminder", trigger='cron', day_of_week=str(weak),
                                        hour=task.hour,
                                        minute=task.minute, second=task.second)
        task.kwargs.pop('dp')
        task.day_of_week = weak
        task.save()
        client_scheduler.print_jobs()
        await dp.bot.send_message(user_id, msg, reply_markup=continue_keyboard)
        logger.info(f"SEND_REMINDER: Отправили уведомление пользователю с id {user_id}")
        return
    elif count == 1:
        month = my_date.month + 1
        client_scheduler.reschedule_job(job_id=f"{user_id}_reminder", trigger='cron', month=str(month),
                                        day_of_week=str(my_date.weekday()),
                                        hour=task.hour,
                                        minute=task.minute, second=task.second)
        task.kwargs.pop('dp')
        task.month = month
        task.save()
        client_scheduler.print_jobs()
        await dp.bot.send_message(user_id, msg, reply_markup=continue_keyboard)
        logger.info(f"SEND_REMINDER: Отправили уведомление пользователю с id {user_id}")
        return
    else:
        logger.info(f"SEND_REMINDER: Отправили уведомление пользователю с id {user_id}. Задача будет удалена.")

        del_scheduler(job_id=f"{user_id}_reminder", where='client')

    # RUS TODO Новые состояния


async def send_test_period_reminder(dp: Dispatcher, user_id: int, msg: str, count: int = 0):
    if PeriodicTask.objects.filter(job_id=f"{user_id}_send_first_code").exists() or PeriodicTask.objects.filter(
            job_id=f"{user_id}_send_code"):
        del_scheduler(job_id=f"{user_id}_send_test_period_reminder", where='client')
    try:
        task = PeriodicTask.objects.get(job_id=f"{user_id}_send_test_period_reminder")
    except PeriodicTask.DoesNotExist:
        logger.critical(
            f"SEND_TEST_PERIOD_REMINDER: Ошибка! Периодической задачи с id {user_id}_send_test_period_reminder не существует")
        return
    task.kwargs['count'] = count + 1
    kwargs = task.kwargs
    kwargs['dp'] = dp
    if count == 1:
        """⚠ Остался 1 день, чтобы завершить подготовку к цели.
         Вы можете бесконечно присылать кружки на проверку,
          но важно пройти этап подготовки не более чем за 6 дней,
           иначе на 7 день спор будет проигран."""
        kwargs[
            'msg'] = f"⚠ Осталось {7 - count - 1} дней, чтобы завершить подготовку к цели. Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6 дней, иначе на 7 день спор будет проигран."
    elif count in [2, 3, 4]:
        kwargs[
            'msg'] = f"⚠ Осталось {7 - count - 1} дня, чтобы завершить подготовку к цели. Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6 дней, иначе на 7 день спор будет проигран."
    elif count == 5:
        kwargs[
            'msg'] = f"⚠ Остался {7 - count - 1} день, чтобы завершить подготовку к цели. Вы можете бесконечно присылать кружки на проверку, но важно пройти этап подготовки не более чем за 6 дней, иначе на 7 день спор будет проигран."
    elif count == 6:

        # TODO Нужно сменить статус пользователя потому что он проиграл. Обработать логику завершения игры

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            logger.critical(
                f"SEND_TEST_PERIOD_REMINDER: Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User")

            return
        # TODO Вставить логику снятия денег после подруба библы
        logger.info(f"Пользователь {user_id} проиграл по причине: 'Не было отправлено тестовое видео'")
        user.count_mistakes = 0
        user.deposit = 0
        user.save()
        msg = f'Время на подготовку к цели истекло'
        await dp.bot.send_message(user_id, msg, reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='👍 Больше не повторится', callback_data='new_dispute_after_finish')
        ))
        del_scheduler(job_id=f"{user_id}_send_test_period_reminder", where='client')

    else:
        await dp.bot.send_message(user_id, msg,
                                  reply_markup=types.InlineKeyboardMarkup().add(
                                      types.InlineKeyboardButton(text='Отправить видео',
                                                                 callback_data="lets_start_training")))
        logger.info(
            f"SEND_TEST_PERIOD_REMINDER: отправили уведомление пользователю с id {user_id}")
        client_scheduler.modify_job(job_id=f"{user_id}_send_test_period_reminder", kwargs=kwargs)
        task.kwargs.pop('dp')
        task.save()


def date_calculated(notification_hour, utc_hour, date):
    if notification_hour < int(utc_hour):
        date -= 1
    if date == -1:
        date = 6

    return date


async def init_send_code(user_id, chat_id, when: str, id_video: int, t_zone: str, notification_hour: int = None,
                         notification_min: int = None):
    hour, minute, second = time_calculated(t_zone, notification_hour, notification_min)
    if TEST:
        logger.debug(
            f"INIT_SEND_CODE: Была инициализирована отправка кода в тестовом режиме для пользователя с id {user_id}")
        hour, minute, second = time_calculated(t_zone)
        minute = int(minute) + 5
        if minute >= 60:
            hour = str(int(hour) + 1)
            minute %= 60
        minute = str(minute)
        day_of_week = '*'
    elif when == "послезавтра":
        my_date = date.today()
        day_of_week = date_calculated(notification_hour, hour, (my_date.weekday() + 2) % 7)
        logger.info(
            f"INIT_SEND_CODE: Была инициализирована отправка кода для пользователя с id {user_id}. Начало ПОСЛЕЗАВТРА DAY: {day_of_week}")
    else:
        logger.info(
            f"INIT_SEND_CODE: Была инициализирована отправка кода для пользователя с id {user_id}. Начало ПОНЕДЕЛЬНИК")
        day_of_week = date_calculated(notification_hour, hour, 0)

    kwargs = {'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video}
    PeriodicTask.objects.create(user_id=user_id, job_id=f'{user_id}_{"send_first_code"}', fun="send_first_code",
                                day_of_week=str(day_of_week),
                                hour=hour,
                                minute=minute, second=second, is_change=True,
                                kwargs=kwargs)
    logger.info(f"ADD_JOB: Добавили задачу send_first_code для пользователя с id: {user_id}")
    admin_scheduler.print_jobs()
    PeriodicTask.objects.filter(job_id=f'{user_id}_send_test_period_reminder').delete()


def load_periodic_task_for_admin():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        if task.fun == "send_code":
            admin_scheduler.add_job(send_code, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "send_first_code":
            admin_scheduler.add_job(send_first_code, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "soft_deadline_reminder":
            admin_scheduler.add_job(soft_deadline_reminder, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "hard_deadline_reminder":
            admin_scheduler.add_job(hard_deadline_reminder, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        logger.info(f"LOAD_PERIODIC_TASK_FOR_ADMIN: Периодические задачи подгружены")
        logger.debug(f"{client_scheduler.print_jobs()}")


def load_periodic_task_for_client():
    periodic_tasks_list = PeriodicTask.objects.all()

    for task in periodic_tasks_list:
        kwargs = task.kwargs
        if task.fun == "reminder":
            kwargs['dp'] = dp
            client_scheduler.add_job(send_reminder, replace_existing=True, trigger='cron', id=f'{task.job_id}',
                                     month=task.month,
                                     day_of_week=task.day_of_week,
                                     hour=f'{task.hour}',
                                     minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)
        elif task.fun == "send_test_period_reminder":
            print(task.fun)
            kwargs['dp'] = dp
            client_scheduler.add_job(send_test_period_reminder, replace_existing=True, trigger='cron',
                                     id=f'{task.job_id}',
                                     month=task.month,
                                     day_of_week=task.day_of_week,
                                     hour=f'{task.hour}',
                                     minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)
        elif task.fun == "send_reminder_after_end":
            print(task.fun)
            kwargs['dp'] = dp
            client_scheduler.add_job(send_reminder_after_end, replace_existing=True, trigger='cron',
                                     id=f'{task.job_id}',
                                     month=task.month,
                                     day_of_week=task.day_of_week,
                                     hour=f'{task.hour}',
                                     minute=f'{task.minute}', second=f'{task.second}', kwargs=task.kwargs)

    logger.info(f"LOAD_PERIODIC_TASK_FOR_CLIENT: Периодические задачи подгружены")
    logger.debug(f"{client_scheduler.print_jobs()}")


async def send_first_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code

    await new_code(chat_id, user_id, id_video)
    scheduler = PeriodicTask.objects.get(job_id=f'{user_id}_send_first_code')
    del_scheduler(f'{user_id}_send_first_code', 'admin')
    add_job(admin_scheduler, call_fun=send_code, str_name='send_code', user_id=user_id,
            day_of_week='*',
            hour=scheduler.hour,
            minute=scheduler.minute,
            second=scheduler.second, kwargs={'user_id': user_id, 'chat_id': chat_id, 'id_video': id_video})
    logger.info(f"SEND_FIRST_CODE: Был отправлен первый код пользователю с id {user_id}")
    add_soft_deadline(user_id)


def add_soft_deadline(user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        logger.critical(f"ADD_SOFT_DEADLINE: Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User")
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
            logger.critical(
                f"ADD_SOFT_DEADLINE: Ошибка: неверное указано утреннее время для пользователя с id {user_id}")
            return f'ADD_SOFT_DEADLINE: Ошибка: неверное указано утреннее время для пользователя с id {user_id}'
    else:
        hour, minute, second = time_calculated(user.timezone, 22, 0)
    add_job(admin_scheduler, call_fun=soft_deadline_reminder, str_name='soft_deadline_reminder', user_id=user_id,
            day_of_week='*',
            hour=hour,
            minute=minute,
            second=second, kwargs={'user_id': user_id})
    logger.info(f"ADD_SOFT_DEADLINE: Был создан мягкий дедлайн для пользователя с id {user_id}")


async def soft_deadline_reminder(user_id):
    instance = RoundVideo.objects.filter(user_tg_id=user_id).last()
    if instance is None:
        logger.critical(f'SOFT_DEADLINE_REMINDER: Ошибка: Отсутствует запись для пользователя с id {user_id}')
        return f'Ошибка: Отсутствует запись для пользователя с id {user_id}'
    if instance.tg_id is None:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            logger.critical(
                f'SOFT_DEADLINE_REMINDER: Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User')
            return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
        await dp.bot.send_message(user_id, f'{user.user_name}, ты всё ещё можешь отправить репорт')

        del_scheduler(job_id=f'{user_id}_soft_deadline_reminder', where='admin')
        logger.info(
            f"SOFT_DEADLINE_REMINDER: Пользователь с id {user_id} не отправил видео в мягкий дедлайн. Был создан жёсткий дедлайн")
        add_hard_deadline(user_id, kwargs={'user_id': user_id, 'id_round_video': instance.id})

    else:
        logger.info(
            f"SOFT_DEADLINE_REMINDER: Пользователь с id {user_id} отправил видео в мягкий дедлайн. Дедлайны удалены")
        del_scheduler(job_id=f'{user_id}_soft_deadline_reminder', where='admin')


def add_hard_deadline(user_id, kwargs):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        logger.critical(f'ADD_HARD_DEADLINE: Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User')
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
            logger.critical(
                f'ADD_HARD_DEADLINE: Ошибка: неверное указано утреннее время для пользователя с id {user_id}')
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


async def hard_deadline_reminder(user_id, id_round_video, time):
    try:
        video = RoundVideo.objects.get(id=id_round_video)
    except RoundVideo.DoesNotExist:
        logger.critical(
            f'HARD_DEADLINE_REMINDER: Ошибка: Из бд была удалена запись с id {id_round_video} для пользователя {user_id}')
        return f'Ошибка: Из бд была удалена запись с id {id_round_video} для пользователя {user_id}'

    if video.tg_id is None:
        # TODO Добавить кнопку "Больше не повторится"
        await dp.bot.send_message(user_id,
                                  f'Время для отправки репорта истекло. По правилам Диспута, мы ждём твой репорт каждый день до {time}',
                                  reply_markup=types.InlineKeyboardMarkup().add(
                                      types.InlineKeyboardButton(text='👍 Больше не повторится',
                                                                 callback_data='try_again')))

        video.status = RoundVideo.VideoStatus.bad
        video.type_video = RoundVideo.TypeVideo.archive
        video.save()
        logger.info(f"HARD_DEADLINE_REMINDER: Пользователь с id {user_id} не отправил видео в срок")

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            logger.critical(
                f'HARD_DEADLINE_REMINDER: Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User')
            return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
        # TODO Выводит полный депозит после проигрыша. Я не понимаю на чьей стороне косяк
        if user.count_mistakes - 1 <= 0:
            logger.info(
                f"HARD_DEADLINE_REMINDER: Пользователь с id {user_id} проиграл диспут по причине: 'Закончилось право на ошибку'")
            del_scheduler(job_id=f'{user_id}_send_code', where='admin')
            user.deposit = 0
            # TODO Вставить логику снятия денег после подруба библы
        user.count_mistakes -= 1
        if user.count_mistakes == 1:
            logger.info(f"HARD_DEADLINE_REMINDER: Пользователь с id {user_id} потерял 20% депозита")
            user.deposit = round(user.deposit - user.deposit / 5)
        user.save()
        del_scheduler(job_id=f'{user_id}_hard_deadline_reminder', where='admin')
    else:
        logger.info(f"HARD_DEADLINE_REMINDER: Пользователь с id {user_id} отправил видео до жёсткого дедлайна")
        del_scheduler(job_id=f'{user_id}_hard_deadline_reminder', where='admin')


async def send_reminder_after_end(dp: Dispatcher, user_id: int, msg: str, count: int = 0):
    try:
        task = PeriodicTask.objects.get(job_id=f"{user_id}_send_reminder_after_end")
    except PeriodicTask.DoesNotExist:
        logger.critical(
            f'SEND_REMINDER_AFTER_END: Ошибка! Периодической задачи с id {user_id}_send_reminder_after_end не существует')
        return f'Ошибка! Периодической задачи с id {user_id}_send_reminder_after_end не существует'

    task.kwargs['count'] = count + 1
    kwargs = task.kwargs
    kwargs['dp'] = dp
    client_scheduler.modify_job(job_id=f"{user_id}_send_reminder_after_end", kwargs=kwargs)
    my_date = date.today()
    if count == 0:

        weak = my_date.weekday()
        client_scheduler.reschedule_job(job_id=f"{user_id}_send_reminder_after_end", trigger='cron',
                                        day_of_week=str(weak),
                                        hour=task.hour,
                                        minute=task.minute, second=task.second)
        task.kwargs.pop('dp')
        task.day_of_week = weak
        task.save()
        client_scheduler.print_jobs()
        await dp.bot.send_message(user_id, msg)
        logger.info(f'SEND_REMINDER_AFTER_END: Пользователю с id {user_id} было отправлено напоминание')
        return
    elif count == 1:
        month = my_date.month + 1
        client_scheduler.reschedule_job(job_id=f"{user_id}_send_reminder_after_end", trigger='cron', month=str(month),
                                        day_of_week=str(my_date.weekday()),
                                        hour=task.hour,
                                        minute=task.minute, second=task.second)
        task.kwargs.pop('dp')
        task.month = month
        task.save()
        client_scheduler.print_jobs()
        await dp.bot.send_message(user_id, msg)
        logger.info(f'SEND_REMINDER_AFTER_END: Пользователю с id {user_id} было отправлено напоминание')
        return
    else:
        logger.info(
            f'SEND_REMINDER_AFTER_END: Пользователю с id {user_id} было отправлено напоминание. Напоминание удалено')

        del_scheduler(job_id=f"{user_id}_reminder", where='client')


async def send_code(user_id: int, chat_id: int, id_video: int):
    from admin.reports.callbacks import new_code
    await new_code(chat_id, user_id, id_video)
    logger.info(
        f'SEND_CODE: Пользователю с id {user_id} был отправлен код')
    add_soft_deadline(user_id)


def del_scheduler(job_id: str, where: str):
    try:
        PeriodicTask.objects.filter(job_id=job_id).delete()

        if where == 'client':
            client_scheduler.remove_job(job_id=job_id)
            logger.debug(f"Удалили задачу с job_id {job_id}. Where= client")
        elif where == 'admin':
            admin_scheduler.remove_job(job_id=job_id)
            logger.debug(f"Удалили задачу с job_id {job_id}. Where= admin")

        else:
            print(f'ERROR: Неверный параметр where')
    except:
        pass


async def change_period_task_info(user_id, time_zone):
    logger.info(f"CHANGE_PERIOD_TASK_INFO: Пользователь с id {user_id} изменил TZ")

    tasks = PeriodicTask.objects.filter(user_id=user_id)

    for task in tasks:

        if task.fun == 'send_first_code':
            hour, minute, second = time_calculated(time_zone, 4, 30)
            if 17 < int(task.hour) <= 23 and 0 < int(hour) <= 14:
                day_of_week = (int(task.day_of_week) + 1) % 7
            elif 0 < int(task.hour) <= 14 and 17 < int(hour) <= 23:
                day_of_week = (int(task.day_of_week) - 1) % 7
            else:
                day_of_week = task.day_of_week
            change_task = PeriodicTask.objects.get(job_id=f'{user_id}_send_first_code')
            change_task.day_of_week = day_of_week
            change_task.hour = hour
            change_task.minute = minute
            change_task.second = second
            change_task.is_change = True
            change_task.save()

        elif task.fun == 'send_code':
            hour, minute, second = time_calculated(time_zone, 4, 30)
            change_task = PeriodicTask.objects.get(job_id=f'{user_id}_send_code')
            change_task.day_of_week = '*'
            change_task.hour = hour
            change_task.minute = minute
            change_task.second = second
            change_task.is_change = True
            change_task.save()
        elif task.fun == 'soft_deadline_reminder':
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                logger.critical(f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User')
                print(f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User')
                continue
            if user.action == 'morning':
                if user.additional_action == 'five_am':
                    hour, minute, second = time_calculated(time_zone, 5, 0)
                elif user.additional_action == 'six_am':
                    hour, minute, second = time_calculated(time_zone, 6, 0)
                elif user.additional_action == 'seven_am':
                    hour, minute, second = time_calculated(time_zone, 7, 0)
                elif user.additional_action == 'eight_am':
                    hour, minute, second = time_calculated(time_zone, 8, 0)
                else:
                    logger.critical(f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}')
                    print(f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}')
                    continue

            else:
                hour, minute, second = time_calculated(time_zone, 22, 0)
            task = PeriodicTask.objects.get(job_id=f'{user_id}_soft_deadline_reminder')
            task.day_of_week = '*'
            task.hour = hour
            task.minute = minute
            task.second = second
            task.is_change = True
            task.save()
        elif task.fun == 'hard_deadline_reminder':
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                logger.critical(f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User')
                return f'Ошибка: Отсутствует запись для пользователя с id {user_id} в таблице User'
            if user.action == 'morning':
                if user.additional_action == 'five_am':
                    hour, minute, second = time_calculated(time_zone, 5, 30)

                elif user.additional_action == 'six_am':
                    hour, minute, second = time_calculated(time_zone, 6, 30)

                elif user.additional_action == 'seven_am':
                    hour, minute, second = time_calculated(time_zone, 7, 30)

                elif user.additional_action == 'eight_am':
                    hour, minute, second = time_calculated(time_zone, 8, 30)

                else:
                    logger.critical(f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}')
                    return f'Ошибка: неверное указано утреннее время для пользователя с id {user_id}'
            else:
                hour, minute, second = time_calculated(user.timezone, 22, 30)
            task = PeriodicTask.objects.get(job_id=f'{user_id}_hard_deadline_reminder')
            task.day_of_week = '*'
            task.hour = hour
            task.minute = minute
            task.second = second
            task.is_change = True
            task.save()
    if client_scheduler.get_job(job_id=f'{user_id}_reminder'):
        hour, minute, second = time_calculated(time_zone, 10, 0)
        client_scheduler.reschedule_job(f'{user_id}_reminder', trigger='cron', day_of_week='*', hour=hour,
                                        minute=minute,
                                        second=second)


async def reload_tasks():
    tasks = PeriodicTask.objects.filter(is_change=True)
    for task in tasks:
        kwargs = task.kwargs
        if task.fun == "send_code":
            admin_scheduler.add_job(send_code, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "send_first_code":
            admin_scheduler.add_job(send_first_code, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "soft_deadline_reminder":
            admin_scheduler.add_job(soft_deadline_reminder, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        elif task.fun == "hard_deadline_reminder":
            admin_scheduler.add_job(hard_deadline_reminder, replace_existing=True, trigger='cron',
                                    day_of_week=task.day_of_week,
                                    hour=task.hour,
                                    minute=task.minute,
                                    second=task.second,
                                    id=task.job_id,
                                    kwargs=kwargs)
        task.is_change = False
        task.save()
    logger.debug(f'RELOAD_TASKS:{admin_scheduler.print_jobs()}')

# TODO Обработать удаление всех напоминалок если пользователь жмёт "Спорить" когда периодическая задача уже создана
