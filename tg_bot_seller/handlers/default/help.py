from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from tg_bot_seller.loader import dp
from tg_bot_seller.filters.admin import AdminFilter


@dp.message_handler(CommandHelp(), AdminFilter())
async def bot_help_admin(message: types.Message):
    text = (
        "Список команд администратора: ",
        "/help - Получить справку",
        "/order - Купить BTC",
        "/set_card - Сменить реквизиты карты",
        "/set_rate - Сменить курс обмена"
    )

    await message.answer("\n".join(text))


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = (
        "Список команд: ",
        "/start - Начать диалог",
        "/help - Получить справку",
        "/order - Купить BTC"
    )

    await message.answer("\n".join(text))
