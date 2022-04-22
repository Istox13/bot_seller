import logging
import math
import decimal

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext

from tg_bot_seller.loader import dp
from tg_bot_seller.keyboards.inline import confirmation, cancel, wallets
from tg_bot_seller.utils.notify_admin import new_order_notify
from tg_bot_seller.utils.validate_wallet import validate_wallet
from tg_bot_seller.models.commands import DBCommands
from tg_bot_seller.states.purchase import Purchase


@dp.message_handler(Command('order'))
async def create_purchase(message: types.Message, state: FSMContext = None):
    text = "\n".join(
        [
            "Укажите сумму в BTC или же RUB: ",
            "",
            "Пример: 0.001 или 0, 001 или 5030"
        ]
    )

    await message.answer(
        text=text,
        reply_markup=cancel.keyboard
    )

    await Purchase.input_quantity.set()


@dp.message_handler(state=Purchase.input_quantity)
async def create_purchase(message: types.Message, state: FSMContext):
    MIN_QUANTITY_BTC = 0.0001
    MAX_QUANTITY_BTC = 0.3

    answer = message.text.replace(",", ".")

    try:
        quantity = float(answer)
    except ValueError:
        text = "\n".join(
            [
                "Некорректная сумма ",
                "",
                "Пример: 0.001 или 0,001 или 5030"
            ]
        )

        await message.answer(
            text=text,
            reply_markup=cancel.keyboard
        )

        return

    rate = await DBCommands.get_rate()

    min_quantity_rub = math.ceil(MIN_QUANTITY_BTC * rate)
    max_quantity_rub = math.ceil(MAX_QUANTITY_BTC * rate)

    is_rub_quantity = min_quantity_rub <= quantity <= max_quantity_rub

    if is_rub_quantity:
        amount = quantity
        quantity = float(str(decimal.Decimal(quantity / rate))[:9])
    else:
        amount = math.ceil(quantity * rate)

    if not (MIN_QUANTITY_BTC <= quantity <= MAX_QUANTITY_BTC) or (not is_rub_quantity and len(answer) > 9):
        await message.answer("Некорректная сумма!")

        text = "\n".join(
            [
                f"Минимальное колличество BTC для покупки: {MIN_QUANTITY_BTC} ",
                f"Максимальное колличество BTC для покупки: {MAX_QUANTITY_BTC} ",
                "",
                f"Вы пытаетесь купить {quantity} BTC"
            ]
        )

        await message.answer(
            text=text,
            reply_markup=cancel.keyboard
        )

        return

    await state.update_data({
        "amount": amount,
        "quantity": quantity,
        "rate": rate
    })

    text = "\n".join(
        [
            f"Средний рыночный курс BTC {rate} руб. ",
            "",
            f"Вы получите: {quantity} BTC"
        ]
    )

    await message.answer(
        text=text
    )

    user_wallets = await DBCommands.get_wallets()
    wallets_keyboard = wallets.get_wallets_keyboard(user_wallets)

    await message.answer(
        text="Скопируйте и отправьте боту свой кошелек BTC. \n"
             "Бот сохранит его и при следующем обмене предложит в виде удобной кнопки ниже:",
        reply_markup=wallets_keyboard
    )

    await Purchase.input_wallet.set()


@dp.message_handler(state=Purchase.input_wallet)
async def input_wallet(message: types.Message, state: FSMContext):
    address = message.text

    if not await validate_wallet(address):
        await message.answer("Неверный адрес кошелька \n\nПопробуйте еще раз")
        return

    user = await DBCommands.get_user()

    if not user:
        await DBCommands.create_user(address)
    else:
        await DBCommands.add_wallet(address, user.id)

    await state.update_data({"address": address})

    data = await state.get_data()

    text = "\n".join(
        [
            f"Итого к оплате: {data.get('amount')} руб. ",
            "",
            f"После оплаты средства будут переведены на кошелек: {address}",
            "",
            "Вы согласны на обмен?"
        ]
    )

    await message.answer(
        text=text,
        reply_markup=confirmation.keyboard
    )

    await Purchase.confirmation.set()


@dp.callback_query_handler(text_contains="confirm", state=Purchase.confirmation)
async def confirm_purchase(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete_reply_markup()
    card_number = await DBCommands.get_card()
    data = await state.get_data()
    user = await DBCommands.get_user()

    await DBCommands.create_purchase(
        user_id=user.id,
        wallet=data.get("address"),
        quantity=data.get("quantity"),
        amount=data.get("amount")
    )
    await new_order_notify(
        dp=dp,
        user_name=user.username,
        wallet=data.get("address"),
        quantity=data.get("quantity"),
        amount=data.get("amount")
    )

    await callback_query.message.answer(f"Переведите {data.get('amount')} RUB \n\nНа карту {card_number}")
    await state.finish()


@dp.callback_query_handler(text_contains="cancel", state=Purchase.all_states)
async def cancel_purchase(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Сделка отменена")
    await callback_query.message.delete_reply_markup()
    await state.finish()


@dp.callback_query_handler(text_contains="wallet", state=Purchase.input_wallet)
async def chose_wallet(callback_query: types.CallbackQuery, state: FSMContext):
    wallet = callback_query.data.split(":")[1]
    await callback_query.message.delete()

    data = await state.get_data()

    await state.update_data({"address": wallet})

    text = "\n".join(
        [
            f"Итого к оплате: {data.get('amount')} руб. ",
            "",
            f"После оплаты средства будут переведены на кошелек: {wallet}",
            "",
            "Вы согласны на обмен?"
        ]
    )

    await callback_query.message.answer(
        text=text,
        reply_markup=confirmation.keyboard
    )

    await Purchase.confirmation.set()
