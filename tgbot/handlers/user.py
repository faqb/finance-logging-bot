from aiogram import Dispatcher
from aiogram.types import Message


async def user(message: Message):
    await message.answer("Private bot. Contact: git/flbot")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user, state="*")
