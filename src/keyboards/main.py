from enum import StrEnum
from functools import lru_cache

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class MAIN_BUTTONS(StrEnum):
    ALL_TOKENS = "Все токены"
    ALL_ADMINS = "Все администраторы"
    HELP = "Помощь"


@lru_cache(maxsize=1)
def get_main_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=MAIN_BUTTONS.ALL_TOKENS),
            KeyboardButton(text=MAIN_BUTTONS.ALL_ADMINS)
        ],
        [
            KeyboardButton(text=MAIN_BUTTONS.HELP)
        ],
    ])
