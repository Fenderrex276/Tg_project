from django.db import models


class RoundVideo(models.Model):
    class VideoStatus(models.TextChoices):
        good = 'good'
        bad = 'bad'
    tg_id = models.CharField(max_length=90)
    user_tg_id = models.IntegerField()
    chat_tg_id = models.IntegerField()
    status = models.CharField('Статус кружочка', max_length=20, choices=VideoStatus.choices)


