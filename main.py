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


# greet user by his name
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


# Function to extract an archive
async def extract_archive(archive_file, output_dir):
    if not os.path.exists(archive_file):
        print(f"Archive {archive_file} not found")
        return
    try:
        # using patool to unpack archive
        patoolib.extract_archive(archive_file, outdir=output_dir)
        print(f"Archive {archive_file} unzipped to {output_dir}")
    except Exception as e:
        print(f"Error unzipping {archive_file}: {str(e)}")


async def process_files(input_dir, output_file):
    # Open the output file for appending in UTF-8 encoding
    async with aiofiles.open(output_file, 'a', encoding='utf-8') as output:
        # Iterate through the files and subdirectories in the input directory
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                input_file = os.path.join(root, filename)

                try:
                    # Open the input file in binary mode to read its content
                    with open(input_file, 'rb') as file:
                        data = file.read()
                        # Detect the encoding of the file's content using chardet
                        detected_encoding = chardet.detect(data)
                        # Check if the detected encoding is confident enough (confidence > 0.5)
                        if detected_encoding['confidence'] > 0.5:
                            encoding = detected_encoding['encoding']
                            # Open the input file again with the detected encoding
                            async with aiofiles.open(input_file, 'r', encoding=encoding) as input:
                                lines = await input.readlines()
                                if lines:
                                    first_line = lines[0]
                                    # Get the file extension (type) from the filename
                                    file_extension = os.path.splitext(filename)[1]
                                    # Add the file extension to the first line
                                    modified_first_line = f"{first_line.strip()} {file_extension}\n"
                                    # Write the modified line to the output file
                                    await output.write(modified_first_line)
                except Exception as e:
                    print(f"Error processing {input_file}: {str(e)}")

# Function to handle incoming documents
async def message_handler(message: Message) -> None:
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="C:/my_folder/arcihvebot/downloads/test.7z")

    archive_file = "downloads/test.7z"
    output_dir = "downloads/"
    output_file = 'downloads/combined_output.txt'

    # Extract the archive and process the files
    await extract_archive(archive_file, output_dir)

    await process_files(output_dir, output_file)
    # Send the processed document back to the user
    await send_message_handler(message, bot)


# send proccessed document back to user
async def send_message_handler(message: Message, bot: Bot):
    txtfile = FSInputFile('downloads/combined_output.txt')
    await bot.send_document(message.chat.id, txtfile)


# Main entry point
async def main() -> None:
    # Register message handlers for processing and sending messages
    dp.message.register(message_handler)
    dp.message.register(send_message_handler)

    await dp.start_polling(bot)


# Start the bot when the script is run
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
