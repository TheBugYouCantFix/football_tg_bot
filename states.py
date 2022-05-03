from aiogram.dispatcher.filters.state import StatesGroup, State


class ActionsStates(StatesGroup):
    start = State()
    begin = State()

    wr = State()  # win rate
    top = State()  # top n countries by win rate
    country_graph = State()

    yes_no = State()


class WinRateStates(StatesGroup):
    choose_country = State()
    choose_year = State()


class TopGraphStates(StatesGroup):
    choose_n = State()



