import logging

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext

from tg_bot_seller.loader import dp, config
from tg_bot_seller.keyboards.inline import confirmation, cancel
from tg_bot_seller.models.commands import DBCommands
from tg_bot_seller.states.set_card import SetCard
from tg_bot_seller.filters.admin import AdminFilter
from tg_bot_seller.utils.validate_card import validate_card


@dp.message_handler(Command("set_card"), AdminFilter())
async def set_rate(message: types.Message, state: FSMContext):
    await message.answer(
        text="Введите новый номер карты",
        reply_markup=cancel.keyboard
    )

    await SetCard.input_new_card.set()


@dp.message_handler(state=SetCard.input_new_card)
async def input_new_rate(message: types.Message, state: FSMContext):
    new_card = message.text.replace(",", ".")

    if validate_card(new_card):
        await message.answer(
            text="Некорректный курс",
            reply_markup=cancel.keyboard
        )

        return

    await state.update_data(
        {
            "new_card": new_card
        }
    )

    old_card = await DBCommands.get_card()

    await message.answer(
        text='\n'.join(
            [
                f"Старый номер карты: {old_card} ",
                f"Новый номер карты: {new_card}"
            ]
        ),
        reply_markup=confirmation.keyboard
    )

    await SetCard.confirmation.set()


@dp.message_handler(state=SetCard.input_password)
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
    new_card = data.get("new_card")

    await DBCommands.set_card(new_card)
    await message.answer(text=f"Карта изменена \n\nНовый номер карты: {new_card}")
    await state.reset_state()


@dp.callback_query_handler(text_contains="confirm", state=SetCard.confirmation)
async def confirm_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="Введите пароль администратора",
        reply_markup=cancel.keyboard
    )

    await callback_query.message.delete_reply_markup()
    await SetCard.input_password.set()


@dp.callback_query_handler(text_contains="cancel", state=SetCard.all_states)
async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete_reply_markup()
    await state.finish()
