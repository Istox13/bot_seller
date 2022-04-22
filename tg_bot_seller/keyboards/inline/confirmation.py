from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить",
                callback_data="confirm"
            ),
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel"
            )
        ]
    ],
    row_width=2
)
