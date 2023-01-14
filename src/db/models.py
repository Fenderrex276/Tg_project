from django.db import models


class RoundVideo(models.Model):
    class VideoStatus(models.TextChoices):
        good = 'good'
        bad = 'bad'
        other = 'other'

    class TypeVideo(models.TextChoices):
        test = "test"
        dispute = "dispute"
        archive = "archive"

    tg_id = models.CharField(max_length=90, null=True, blank=True)
    user_tg_id = models.BigIntegerField()
    chat_tg_id = models.BigIntegerField()
    code_in_video = models.CharField(max_length=4)
    status = models.CharField('Статус кружочка', max_length=20, choices=VideoStatus.choices)
    id_video = models.IntegerField()
    type_video = models.CharField('Тип видео', max_length=20, choices=TypeVideo.choices, default="none")
    n_day = models.IntegerField(default=0)


class User(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя в Телеграмм")
    user_name = models.CharField(max_length=20, verbose_name="Имя пользователя")
    action = models.CharField(max_length=20, verbose_name="Тип диспута")
    additional_action = models.CharField(max_length=20, verbose_name="Дополнительное условие диспута")
    start_disput = models.CharField(max_length=10, verbose_name="Когда начинается диспут")
    deposit = models.IntegerField(verbose_name="Сумма депозита")
    promocode_user = models.CharField(max_length=10, verbose_name="Промокод пользователя")
    promocode_from_friend = models.CharField(max_length=10, verbose_name="Промокод-приглашение")
    count_days = models.IntegerField(verbose_name="Сколько дней длится диспут")
    number_dispute = models.CharField(max_length=6, verbose_name="уникальный идентификатор диспута")
    timezone = models.CharField(max_length=7, verbose_name='Таймзона')
    count_mistakes = models.IntegerField(verbose_name='количество попыток')


class PeriodicTask(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя в Телеграмм")
    fun = models.CharField(max_length=20, verbose_name="Название периодической функции")
    job_id = models.CharField(max_length=255, verbose_name="id задачи")
    day_of_week = models.CharField(max_length=20, default="*", verbose_name="В какой час вызвать")
    hour = models.CharField(max_length=20, default="*", verbose_name="В какой час вызвать")
    minute = models.CharField(max_length=20, default="*", verbose_name="В какую минуту вызвать")
    second = models.CharField(max_length=20, default="*", verbose_name="В какую секунду вызвать")
    kwargs = models.JSONField(verbose_name="Переменные, которые передаются в функцию")


class Support(models.Model):
    class TypeSolve(models.TextChoices):
        new = "new"
        done = "done"
        in_process = "in_process"

    user_id = models.BigIntegerField()
    number_dispute = models.CharField(max_length=6)
    chat_id = models.BigIntegerField()
    problem = models.CharField(max_length=256)
    solved = models.CharField('статус вопроса', choices=TypeSolve.choices, max_length=10)


class Supt(models.Model):
    class TypeSolve(models.TextChoices):
        new = "new"
        done = "done"
        in_process = "in_process"

    user_id = models.BigIntegerField()
    number_dispute = models.CharField(max_length=6)
    chat_id = models.BigIntegerField()
    problem = models.CharField(max_length=256)
    solved = models.CharField('статус вопроса', choices=TypeSolve.choices, max_length=10)


class Reviews(models.Model):
    class StateReview(models.TextChoices):
        done = "done"
        bad_review = "bad_review"
        new = "new"

    user_id = models.BigIntegerField()
    chat_id = models.BigIntegerField()
    user_name = models.CharField(max_length=20, verbose_name="Имя игрока")
    id_dispute = models.IntegerField(verbose_name="Уникальный идентификатор диспута")
    city = models.CharField(max_length=30, verbose_name="Город игрока")
    mark = models.CharField(max_length=10, verbose_name="кол-во звёзд")
    coment = models.CharField(max_length=256, verbose_name="комментарий")
    state_t = models.CharField(max_length=10, verbose_name="статус отзыва", choices=StateReview.choices)
