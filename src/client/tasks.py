from apscheduler.schedulers.background import BackgroundScheduler


def scheduler_init():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_content, 'cron', minute="*")
    scheduler.start()


def send_content():
    # Когда нужно присылать уведомления и откуда их брать
    print("Если ты это читаешь в консольке, то периодический таск работает")


def send_code():
    # Где-то есть генератор кодов, надо найти
    pass


def send_reminder():
    # Нужно покумекать как определять кто уже прошёл проверку, а кто ещё нет, желательно эффективно
    pass
