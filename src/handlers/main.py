from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from database.models import Admin
from database.models.bitrix_token import BitrixToken
from keyboards.main import get_main_keyboard, MAIN_BUTTONS
from middlewares import create_router

from tools.telegram import get_username

__all__ = ["router"]

router = create_router(is_admin=True)


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
    await message.answer(text="Admin panel", reply_markup=get_main_keyboard())


@router.message(F.text == MAIN_BUTTONS.ALL_ADMINS)
async def cmd_all_admins(message: Message) -> None:
    admins: list[Admin] = await Admin.all()
    output: list[str] = [
        f'{i + 1}. @{await get_username(message.bot, obj.id_tg)}'
        for i, obj in enumerate(admins)
    ]
    output_str= '\n'.join(output) if output else "Пустой список"
    await message.answer(f"Все администраторы проекта: \n{output_str}")


@router.message(F.text == MAIN_BUTTONS.ALL_TOKENS)
async def cmd_all_tokens(message: Message) -> None:
    tokens: list[BitrixToken] = await BitrixToken.all()
    output: list[str] = [
        f'{i + 1}. <code>{obj.value}</code>'
        for i, obj in enumerate(tokens)
    ]
    output_str = '\n'.join(output) if output else "Пустой список"
    await message.answer(f"Токены Bitrix: \n{output_str}")
