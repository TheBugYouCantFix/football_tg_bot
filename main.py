import logging
import asyncio
from aiojobs import create_scheduler
from utils import get_scheduler

from datetime import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import Config
from aiogram import Bot, Dispatcher, executor, types

from parsing_data import InternationalMatchesParser

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

imp = InternationalMatchesParser()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f'Hello and welcome, {message.from_user.first_name} {message.from_user.last_name}!'
    )


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    # TODO: write about message
    about_message = ''
    await message.answer(about_message)


@dp.message_handler(commands=['win_rate'])
async def win_rate(message: types.Message):
    try:
        text = message.text.replace('/win_rate ', '')
        country = text[:text.find('since')].strip()
        year = text.split()[-1]
        print(country, year)

        win_rate = imp.get_country_win_rate(country)

        if year.isdigit():
            win_rate = imp.get_country_win_rate(country, int(year))

        ans = f"Win rate of {country} national team: " \
              f"{win_rate}%"

        await message.answer(ans)

    except Exception as e:
        print(e)
        await message.answer("Something went wrong."
                             " Please, check if the country name is correct and try again")


if __name__ == '__main__':
    logging.getLogger('startup').info("Starting via pooling")
    executor.start_polling(dp)
