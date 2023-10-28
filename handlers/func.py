from aiogram.types import Message
from aiogram.utils.markdown import hbold

async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")