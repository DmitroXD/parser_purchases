from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def get_username(bot: Bot, user_id: int):
    try:
        chat = await bot.get_chat(chat_id=user_id)
        return chat.username
    except TelegramBadRequest:
        return None
