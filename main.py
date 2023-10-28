import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from settings import settings
from handlers.func import command_start_handler

TOKEN = settings.bots.bot_token

dp = Dispatcher()



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.message.register(command_start_handler)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())