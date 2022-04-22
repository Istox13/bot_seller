from aiogram.dispatcher.filters import BoundFilter

from tg_bot_seller.loader import config


class AdminFilter(BoundFilter):
    async def check(self, obj) -> bool:
        return obj.from_user.id == config.bot_config.admin_id
