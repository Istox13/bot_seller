from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel"
            )
        ]
    ]
)
