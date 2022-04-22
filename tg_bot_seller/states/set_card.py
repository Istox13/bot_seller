from aiogram.dispatcher.filters.state import StatesGroup, State


class SetCard(StatesGroup):
    input_new_card = State()
    confirmation = State()
    input_password = State()
