import logging
from logging_setup import setup_logging

from aiogram.dispatcher import FSMContext

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import Config
from aiogram import Bot, Dispatcher, executor, types

from parsing_data import InternationalMatchesParser
from states import ActionsStates, WinRateStates

setup_logging()
main_logger = logging.getLogger('main_logger')


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

imp = InternationalMatchesParser()


@dp.message_handler(commands=['about'], state='*')
async def about(message: types.Message):
    about_message = """
    I am a bot that provides some interesting date about football national teams.
Try out some of my commands.
Press "/" to see the typehints of the commands and their description.
    """

    await message.answer(about_message)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):

    await message.answer(
        f'Hello and welcome, {message.from_user.first_name} {message.from_user.last_name}!'
    )

    await select_func(message)


@dp.message_handler(commands=['select_func'])
async def select_func(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('Win rate', callback_data='wr'))
    keyboard.add(types.InlineKeyboardButton('Country win rate graph', callback_data='sg'))

    await message.answer("Select a function", reply_markup=keyboard)
    await ActionsStates.start.set()


@dp.callback_query_handler(state=ActionsStates.start)
async def choose(message: types.CallbackQuery):
    if message.data == 'wr':
        await bot.send_message(message.from_user.id,
                               "Input the country")
        await ActionsStates.wr.set()


@dp.message_handler(state=ActionsStates.wr)
async def get_year(message: types.Message, state: FSMContext):
    country = message.text

    # Validating input
    if imp.matches_played(imp.df, country) == 0:
        await message.answer("No such team found. Please, check if the country name is correct and try again")
        await bot.send_message(message.from_user.id,
                               "Input the country")
        await ActionsStates.wr.set()
        return

    await message.answer("Select a year")
    await WinRateStates.choose_year.set()

    await state.update_data(country=country)


@dp.message_handler(state=WinRateStates.choose_year)
async def win_rate(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    try:
        data = await state.get_data()
        country = data.get('country').strip()

        year = message.text
        main_logger.info(year)

        if not year.isdigit() or not imp.year_is_valid(int(year)):
            year = imp.START_YEAR  # default year (data in csv file starts from it)

        df = imp.after_year(int(year))
        rate = imp.get_country_win_rate(df, country)

        since_year = f'since {year} '

        main_logger.info(country)

        ans = f"Win rate of {country.capitalize()} national team {since_year}: " \
              f"{rate}%"

        await message.answer(ans)
        await state.finish()

    except Exception as e:
        main_logger.error(e)
        await message.answer("Something went wrong."
                             " Please, check if the country name is correct and try again")


if __name__ == '__main__':
    logging.getLogger('startup').info("Starting via pooling")
    executor.start_polling(dp)
