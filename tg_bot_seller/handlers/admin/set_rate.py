import logging

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext

from tg_bot_seller.loader import dp, config
from tg_bot_seller.keyboards.inline import confirmation, cancel
from tg_bot_seller.models.commands import DBCommands
from tg_bot_seller.filters.admin import AdminFilter
from tg_bot_seller.states.set_rate import SetRate


@dp.message_handler(Command("set_rate"), AdminFilter())
async def set_rate(message: types.Message, state: FSMContext):
    await message.answer(
        text="Введите новой курс BTC-RUB",
        reply_markup=cancel.keyboard
    )

    await SetRate.input_new_rate.set()


@dp.message_handler(state=SetRate.input_new_rate)
async def input_new_rate(message: types.Message, state: FSMContext):
    answer = message.text.replace(",", ".")

    try:
        rate = float(answer)
    except ValueError:
        await message.answer(
            text="Некорректный курс",
            reply_markup=cancel.keyboard
        )

        return

    await state.update_data(
        {
            "new_rate": rate
        }
    )

    old_rate = await DBCommands.get_rate()

    await message.answer(
        text='\n'.join(
            [
                f"Старый курс: {old_rate} RUB ",
                f"Новый курс: {rate} RUB"
            ]
        ),
        reply_markup=confirmation.keyboard
    )

    await SetRate.confirmation.set()


@dp.message_handler(state=SetRate.input_password)
async def input_password(message: types.Message, state: FSMContext):
    password = message.text
    await message.delete()

    if password != config.bot_config.admin_password:
        await message.answer(
            text="Неверный пароль \nПопробуйте снова",
            reply_markup=cancel.keyboard
        )

        return

    data = await state.get_data()
    new_rate = data.get("new_rate")

    await DBCommands.set_rate(new_rate)
    await message.answer(text=f"Курс изменен \n\nНовый курс: {new_rate}")
    await state.reset_state()


@dp.callback_query_handler(text_contains="confirm", state=SetRate.confirmation)
async def confirm_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="Введите пароль администратора",
        reply_markup=cancel.keyboard
    )

    await callback_query.message.delete_reply_markup()
    await SetRate.input_password.set()


@dp.callback_query_handler(text_contains="cancel", state=SetRate.all_states)
async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete_reply_markup()
    await state.finish()
