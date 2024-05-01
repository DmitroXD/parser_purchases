from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from database.models import Admin


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        if not user:
            return handler(event, data)
        admin = await Admin.get_or_none(id_tg=user.id)
        if admin:
            return await handler(event, data)
        return None
