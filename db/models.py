from django.db import models


class RoundVideo(models.Model):
    class VideoStatus(models.TextChoices):
        good = 'good'
        bad = 'bad'
    tg_id = models.IntegerField()
    user_tg_id = models.IntegerField()
    transaction_type = models.CharField('Статус кружочка', max_length=20, choices=VideoStatus.choices)