import django

django.setup()

from admin.initialize import bot, dp
from admin.bot import AdminDisputeBot

AdminDisputeBot(bot, dp).start()
