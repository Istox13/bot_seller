from aiogram import executor

from tg_bot_seller.loader import dp
from tg_bot_seller import middlewares, filters, handlers
import tg_bot_seller.models
from tg_bot_seller.utils.database import create_db
from tg_bot_seller.utils.notify_admin import on_startup_notify, on_shutdown_notify
from tg_bot_seller.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляем про запуск
    await on_startup_notify(dispatcher)

    # Инициализируем БД
    await create_db()


def run_bot():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown_notify)


if __name__ == '__main__':
    run_bot()
