import asyncio
from threading import Thread
from typing import Callable, Coroutine

from errors.awaitable import StopLoopingAsync

type AwaitFunc[T] = Callable[[T], Coroutine] | Callable[[], Coroutine]


def run_awaitable_in_thread[*T](func: AwaitFunc[T], *args: T):
    thread = Thread(target=asyncio.run, args=(func(*args), ))
    thread.start()
    return thread


async def run_async_forever[*T](func: AwaitFunc[T], *args: T, timeout: float):
    while True:
        try:
            await func(*args)
        except StopLoopingAsync:
            return None
        await asyncio.sleep(timeout)
