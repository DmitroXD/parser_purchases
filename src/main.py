import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings
from database import async_database_init
from handlers import register_handlers
from tasks import run_tasks

logging.basicConfig(level=logging.INFO)


async def on_startup(bot: Bot):
    if settings.BOT_WEBHOOK_URL:
        await bot.set_webhook(url=settings.BOT_WEBHOOK_URL, drop_pending_updates=False)
    else:
        await bot.delete_webhook(drop_pending_updates=False)


def _get_storage():
    if settings.REDIS_PATH:
        return RedisStorage.from_url(settings.REDIS_PATH)
    return MemoryStorage()


def main(token: str):
    asyncio.new_event_loop().run_until_complete(async_database_init(settings.MYSQL_PATH))
    bot = Bot(token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=_get_storage())
    dp.startup.register(on_startup)
    register_handlers(dp)
    run_tasks()
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    main(settings.BOT_TOKEN)
