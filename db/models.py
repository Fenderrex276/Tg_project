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
    tg_id = models.CharField(max_length=90)
    user_tg_id = models.IntegerField()
    chat_tg_id = models.IntegerField()
    code_in_video = models.CharField(max_length=4)
    status = models.CharField('Статус кружочка', max_length=20, choices=VideoStatus.choices)
    id_video = models.IntegerField()
    type_video = models.CharField('Тип видео', max_length=20, choices=TypeVideo.choices, default="none")


class Users(models.Model):

    user_id = models.IntegerField()
    user_name = models.CharField(max_length=20)
    action = models.CharField(max_length=20)
    additional_action = models.CharField(max_length=20)
    start_disput = models.CharField(max_length=10)
    deposit = models.IntegerField()
    promocode_user = models.CharField(max_length=10)
    promocode_from_friend = models.CharField(max_length=10)
    count_days = models.IntegerField()
    number_dispute = models.CharField(max_length=6)

