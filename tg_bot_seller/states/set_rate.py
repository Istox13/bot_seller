from aiogram.dispatcher.filters.state import StatesGroup, State


class SetRate(StatesGroup):
    input_new_rate = State()
    confirmation = State()
    input_password = State()
