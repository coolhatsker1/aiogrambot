import logging
import sys
import asyncio
import aiofiles
import os
import chardet
import patoolib
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from settings import settings

TOKEN = settings.bots.bot_token
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


async def extract_archive(archive_file, output_dir):
    if not os.path.exists(archive_file):
        print(f"Архів {archive_file} не знайдено")
        return
    try:
        # Використовуємо patool для розархівування архіву
        patoolib.extract_archive(archive_file, outdir=output_dir)
        print(f"Архів {archive_file} розархівовано до {output_dir}")
    except Exception as e:
        print(f"Помилка розархівування {archive_file}: {str(e)}")


async def process_files(input_dir, output_file):
    async with aiofiles.open(output_file, 'a', encoding='utf-8') as output:
        for filename in os.listdir(input_dir):
            input_file = os.path.join(input_dir, filename)
            with open(input_file, 'rb') as file:
                data = file.read()
                detected_encoding = chardet.detect(data)
                if detected_encoding['confidence'] > 0.5:
                    encoding = detected_encoding['encoding']
                    async with aiofiles.open(input_file, 'r', encoding=encoding) as input:
                        lines = await input.readlines()
                        if lines:
                            first_line = lines[0]
                            # Отримайте розширення (тип) файлу з імені файлу
                            file_extension = os.path.splitext(filename)[1]
                            # Додайте розширення до першого рядка
                            modified_first_line = f"{first_line.strip()} {file_extension}\n"
                            await output.write(modified_first_line)


async def message_handler(message: Message) -> None:
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="C:/my_folder/arcihvebot/downloads/test.7z")

    archive_file = "C:/my_folder/arcihvebot/downloads/test.7z"  # Змініть на ім'я вашого архіву
    output_dir = "C:/my_folder/arcihvebot/downloads/"  # Каталог для розархівування файлів
    output_file = 'C:/my_folder/arcihvebot/downloads/combined_output.txt'  # Файл, в який додається перший рядок з кожного файлу

    # Розархівуємо архів
    await extract_archive(archive_file, output_dir)

    # Обробляємо файли, додаючи перший рядок та тип файлу до вихідного файлу
    await process_files(output_dir, output_file)

    await send_message_handler(message, bot)


async def send_message_handler(message: Message, bot: Bot):
    txtfile = FSInputFile('downloads/combined_output.txt')
    await bot.send_document(message.chat.id, txtfile)


async def main() -> None:
    dp.message.register(message_handler)
    dp.message.register(send_message_handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())