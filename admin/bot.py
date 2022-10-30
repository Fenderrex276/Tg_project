from .branches import Admin
from aiogram import executor

branches = [Admin]


class AdminDisputeBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        branches_init = [branch(bot, dp) for branch in branches]
        for b in branches_init:
            b.register_commands()
        for b in branches_init:
            b.register_handlers()

    def start(self):
        executor.start_polling(self.dp, skip_updates=True)
