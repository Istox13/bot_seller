from aiogram import types

from .sourse import (
    UserModel,
    ExchangeRateHistoryModel,
    CardNumberHistoryModel,
    PurchaseModel,
    WalletAddressHistory
)


class DBCommands:

    @staticmethod
    async def get_user() -> UserModel:
        user = await UserModel.query.where(
            UserModel.user_tg_id == types.User.get_current().id
        ).gino.first()

        return user

    @staticmethod
    async def get_rate() -> ExchangeRateHistoryModel:
        rate = await ExchangeRateHistoryModel.query.where(ExchangeRateHistoryModel.active).gino.first()

        return rate.exchange_rate if rate else 0

    @staticmethod
    async def get_card() -> CardNumberHistoryModel:
        card = await CardNumberHistoryModel.query.where(CardNumberHistoryModel.active).gino.first()

        return card.card_number if card else "0000 0000 0000 0000"

    @staticmethod
    async def get_wallets():
        user = await DBCommands.get_user()

        if not user:
            return list()

        wallets = await WalletAddressHistory.query.where(
            WalletAddressHistory.user_id == user.id
        ).gino.all()

        return wallets

    @staticmethod
    async def set_rate(new_rate_value):
        old_rate = await ExchangeRateHistoryModel.query\
            .where(ExchangeRateHistoryModel.active).gino.first()

        new_rate = ExchangeRateHistoryModel()
        new_rate.exchange_rate = new_rate_value
        new_rate.active = True

        await new_rate.create()
        if old_rate:
            await old_rate.update(active=False).apply()

    @staticmethod
    async def set_card(new_card_number):
        old_card = await CardNumberHistoryModel.query \
            .where(CardNumberHistoryModel.active).gino.first()

        new_card = CardNumberHistoryModel()
        new_card.exchange_rate = new_card_number
        new_card.active = True

        await new_card.create()
        if old_card:
            await old_card.update(active=False).apply()

    @staticmethod
    async def create_purchase(user_id, wallet, quantity, amount):
        deal = PurchaseModel()

        deal.user_id = user_id
        deal.quantity = quantity
        deal.amount = amount
        deal.wallet = wallet

        await deal.create()

        return deal

    @staticmethod
    async def create_user(wallet):
        user = types.User.get_current()
        old_user = await DBCommands.get_user()

        if old_user:
            return old_user

        new_user = UserModel()
        new_user.user_tg_id = user.id
        if user.username:
            new_user.username = user.username

        await new_user.create()
        await DBCommands.add_wallet(wallet, new_user.id)

        return new_user

    @staticmethod
    async def add_wallet(wallet, user_id):
        new_wallet = WalletAddressHistory()
        new_wallet.user_id = user_id
        new_wallet.address = wallet
        new_wallet.active = True

        await new_wallet.create()

        return new_wallet
