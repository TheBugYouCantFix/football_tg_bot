from aiogram.dispatcher.filters.state import StatesGroup, State


class ActionsStates(StatesGroup):
    start = State()
    begin = State()
    wr = State()  # win rate


class WinRateStates(StatesGroup):
    choose_country = State()
    choose_year = State()
