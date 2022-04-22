from aiogram import types

from tg_bot_seller.loader import dp


@dp.message_handler()
async def incorrect_message(message: types.Message):
    await message.answer("Узнать о возможностях бота можно с помощью команды /help")
