import logging
import asyncio
from aiojobs import create_scheduler
from utils import get_scheduler

from datetime import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет')


if __name__ == '__main__':
    logging.getLogger('startup').info("Starting via pooling")
    executor.start_polling(dp)
