from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    input_quantity = State()
    confirmation = State()
    input_wallet = State()
