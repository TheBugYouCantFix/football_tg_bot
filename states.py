from aiogram.dispatcher.filters.state import StatesGroup, State


class ActionsStates(StatesGroup):
    start = State()
    begin = State()
    wr = State()  # win rate
    top = State()  # top n countries by win rate
    yes_no = State()
    country_graph = State()


class WinRateStates(StatesGroup):
    choose_country = State()
    choose_year = State()
