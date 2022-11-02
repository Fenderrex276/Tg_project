
import django
django.setup()



from admin.initialze import bot, dp
from admin.bot import AdminDisputeBot



AdminDisputeBot(bot, dp).start()
