import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from settings import settings

TOKEN = settings.bots.bot_token
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def message_handler(message: Message) -> None:
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="C:/my_folder/arcihvebot/downloads/test.7z")

async def main() -> None:

    dp.message.register(message_handler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())