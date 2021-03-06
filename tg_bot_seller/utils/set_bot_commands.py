from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начать диалог"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("order", "Купить BTC"),
        ]
    )
