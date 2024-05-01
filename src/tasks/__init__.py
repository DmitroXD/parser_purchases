from typing import Callable, Coroutine
from aiogram import Bot

from . import parser_purchases
from tools.awaitable import run_awaitable_in_thread


tasks: list[Callable[[], Coroutine]] = [
    parser_purchases.main
]


def run_tasks():
    for task in tasks:
        run_awaitable_in_thread(task)
