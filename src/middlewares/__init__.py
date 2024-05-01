from aiogram import Router, BaseMiddleware

from core.config import settings
from .admin_middleware import AdminMiddleware


def __add_middleware(router: Router, middleware: BaseMiddleware, condition: bool):
    if condition is True:
        for observer in router.observers.values():
            observer.middleware.register(middleware)


def create_router(*, is_admin: bool = False):
    router = Router()
    __add_middleware(router, AdminMiddleware(), is_admin and settings.ADMIN_MIDDLEWARE)
    return router

