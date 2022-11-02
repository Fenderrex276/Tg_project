import os

# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()


from initialize import bot, dp
from bot import DisputeBot

#from db.models import RoundVideo

#RoundVideo.objects.create("1", 2, 'good')
DisputeBot(bot, dp).start()
