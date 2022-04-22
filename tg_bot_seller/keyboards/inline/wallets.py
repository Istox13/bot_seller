from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot_seller.models.sourse import WalletAddressHistory


def get_wallets_keyboard(wallets: List[WalletAddressHistory]):
    keyboard_buttons = list()
    for wallet_address in wallets:
        address = wallet_address.address
        wallet_button = [InlineKeyboardButton(text=address, callback_data="wallet:" + address)]

        keyboard_buttons.append(wallet_button)

    keyboard_buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons, row_width=1)
