from .branches import Admin
from aiogram import executor
from reports.branches import Reports
from reports.callbacks import register_callback as rc1
from support_reviews.callbacks import register_callback as rc2
from initialze import scheduler
from .support_reviews.branches import Reviews

branches = [Admin, Reports, Reviews]
callbacks = [rc1, rc2]


class AdminDisputeBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        branches_init = [branch(bot, dp) for branch in branches]
        for b in branches_init:
            b.register_commands()
        for b in branches_init:
            b.register_handlers()
        for call in callbacks:
            call(dp, bot)

    def start(self):
        scheduler.start()
        executor.start_polling(self.dp, skip_updates=True)
