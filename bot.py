from branches.dispute_with_friend.branches import DisputeWithFriend
from branches.pay.branches import Pay
from branches.start.branches import Start
from branches.dispute_with_friend.callbacks import register_callback as rc1
from branches.start.callbacks import register_callback as rc2
from branches.confirm_dispute.callbacks import register_callback as rc3
from branches.pay.callbacks import register_callback as rc4
from branches.confirm_dispute.branches import ConfirmDispute
from aiogram import executor
from branches.training.callbacks import register_callback as rc5
from branches.training.branches import Training

branches = [Start, DisputeWithFriend, ConfirmDispute, Pay, Training]
callbacks = [rc1, rc2, rc3, rc4, rc5]


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
        executor.start_polling(self.dp, skip_updates=True)
