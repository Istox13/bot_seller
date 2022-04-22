import sqlalchemy as sa
from sqlalchemy import sql

from tg_bot_seller.utils.database import db


class BaseModel(db.Model):
    """Parent Model"""

    __abstract__ = True

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        nullable=False,
        comment="Идентификатор",
    )

    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=sa.func.current_timestamp(),
        comment="Дата создания",
    )

    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=sa.func.current_timestamp(),
        onupdate=sa.func.current_timestamp(),
        comment="Дата обновления",
    )
    query: sql

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)


class UserModel(BaseModel):
    __tablename__ = "users"

    user_tg_id = sa.Column(
        sa.BigInteger,
        nullable=False,
        default=0,
        comment="Телеграм идентификатор пользователя"
    )
    username = sa.Column(
        sa.String,
        nullable=True,
        default="",
        comment="Имя пользователя"
    )


class PurchaseModel(BaseModel):
    __tablename__ = "purchases"

    user_id = sa.Column(
        sa.Integer,
        nullable=False,
        default=0,
        comment="Идентификатор из таблицы с пользователями"
    )
    wallet = sa.Column(
        sa.String,
        nullable=True,
        default="",
        comment="Адрес кошелька"
    )
    quantity = sa.Column(
        sa.Float,
        nullable=False,
        default=0.0,
        comment="Колличество BTC"
    )
    amount = sa.Column(
        sa.Float,
        nullable=False,
        default=0.0,
        comment="Стоимость"
    )


class WalletAddressHistory(BaseModel):
    __tablename__ = "wallet_address_history"

    user_id = sa.Column(
        sa.Integer,
        nullable=False,
        default=0,
        comment="Идентификатор из таблицы с пользователями"
    )
    address = sa.Column(
        sa.String,
        nullable=True,
        default="",
        comment="Адрес кошелька"
    )
    active = sa.Column(
        sa.Boolean,
        nullable=False,
        default=False,
        comment="Флаг активности кошелька"
    )


class ExchangeRateHistoryModel(BaseModel):
    __tablename__ = "exchange_rate_history"

    exchange_rate = sa.Column(
        sa.Float,
        nullable=False,
        default=0.0,
        comment="Значение BTC-RUB"
    )
    active = sa.Column(
        sa.Boolean,
        nullable=False,
        default=False,
        comment="Флаг активности курса"
    )


class CardNumberHistoryModel(BaseModel):
    __tablename__ = "card_number_history"

    card_number = sa.Column(
        sa.String,
        nullable=False,
        default="0000 0000 0000 0000",
        comment="Номер карты"
    )
    active = sa.Column(
        sa.Boolean,
        nullable=False,
        default=False,
        comment="Флаг активности карты"
    )
