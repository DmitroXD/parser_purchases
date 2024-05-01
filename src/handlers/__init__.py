from aiogram import Dispatcher, Router

from . import main, cmd

routers: list[Router] = [
    main.router,
    cmd.router
]


def register_handlers(dp: Dispatcher):
    if routers:
        dp.include_routers(*routers)
