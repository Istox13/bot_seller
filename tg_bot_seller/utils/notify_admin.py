import logging

from aiogram import Dispatcher
from aiogram.types import ParseMode

from tg_bot_seller.loader import config


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(config.bot_config.admin_id, "Бот запущен")

    except Exception as err:
        logging.exception(err)


async def on_shutdown_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(config.bot_config.admin_id, "Бот остановлен")

    except Exception as err:
        logging.exception(err)


async def new_order_notify(dp: Dispatcher, user_name, wallet, quantity, amount):
    text = [
        f"Заказ от @{user_name}: \n" if user_name else "Новый заказ: \n",
        f"Кошелек: ```{wallet}``` ",
        f"Заказ на ```{quantity}``` BTC ",
        f"Цена: {amount} RUB"
    ]

    try:
        await dp.bot.send_message(
            config.bot_config.admin_id,
            text='\n'.join(text),
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as err:
        logging.exception(err)


async def notify_admin(dp: Dispatcher, message: str):
    try:
        await dp.bot.send_message(
            config.bot_config.admin_id,
            message,
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as err:
        logging.exception(err)
