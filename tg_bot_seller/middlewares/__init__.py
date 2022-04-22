from aiogram import Dispatcher

from tg_bot_seller.loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
