import logging

from aiogram import executor

from admin.administration.callbacks import register_callback as rc3
from admin.reports.branches import Reports
from admin.reports.callbacks import register_callback as rc1
from admin.support_reviews.branches import Reviews
from admin.administration.branches import Administration
from admin.support_reviews.callbacks import register_callback as rc2
from client.tasks import load_periodic_task_for_admin, reload_tasks
from .branches import Admin
from .initialize import scheduler

branches = [Admin, Reports, Reviews, Administration]
callbacks = [rc1, rc2, rc3]
logger = logging.getLogger(__name__)


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
        logger.info("Admin_bot запущен")
        scheduler.start()
        load_periodic_task_for_admin()

        scheduler.add_job(reload_tasks, replace_existing=True, trigger='cron', id=f'reload_tasks',
                          minute="*")
        scheduler.print_jobs()
        executor.start_polling(self.dp, skip_updates=True)
