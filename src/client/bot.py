import logging

from aiogram import executor

from branches.confirm_dispute.branches import ConfirmDispute
from branches.confirm_dispute.callbacks import register_callback as rc3
from branches.dispute_with_friend.branches import DisputeWithFriend
from branches.dispute_with_friend.callbacks import register_callback as rc1
from branches.knowledge_base.FAQ.callbacks import register_callback as rc13
from branches.knowledge_base.TED.callbacks import register_callback as rc12
from branches.knowledge_base.books.callbacks import register_callback as rc11
from branches.knowledge_base.despair_minute.callbacks import register_callback as rc9
from branches.knowledge_base.films.callbacks import register_callback as rc10
from branches.knowledge_base.memes.callbacks import register_callback as rc8
from branches.knowledge_base.principles_of_success.callbacks import register_callback as rc7
from branches.knowledge_base.supdis.callbacks import register_callback as rc14
from branches.pay.branches import Pay
from branches.pay.callbacks import register_callback as rc4
from branches.start.branches import Start
from branches.start.callbacks import register_callback as rc2
from branches.thirty_days_dispute.branches import CurrentDispute
from branches.thirty_days_dispute.callbacks import register_callback as rc6
from branches.training.branches import Training
from branches.training.callbacks import register_callback as rc5
from client.initialize import scheduler
from client.tasks import load_periodic_task_for_client

branches = [Start, DisputeWithFriend, ConfirmDispute, Pay, Training, CurrentDispute]
callbacks = [rc1, rc2, rc3, rc4, rc5, rc6, rc7, rc8, rc9, rc10, rc11, rc12, rc13, rc14]
logger = logging.getLogger(__name__)


class DisputeBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        branches_init = [branch(bot, dp) for branch in branches]
        for b in branches_init:
            b.register_commands()
        for b in branches_init:
            b.register_handlers()
        for call in callbacks:
            call(bot, dp)

    def start(self):
        logger.info("Client_bot запущен")
        scheduler.start()
        load_periodic_task_for_client()
        executor.start_polling(self.dp, skip_updates=True)
