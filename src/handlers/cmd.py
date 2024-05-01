from aiogram import F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from database.models import BitrixToken, Admin
from keyboards.main import MAIN_BUTTONS
from middlewares import create_router


__all__ = ["router"]


router = create_router(is_admin=True)


@router.message(Command("token"))
async def cmd_add_token(message: Message, command: CommandObject):
    await BitrixToken(value=command.args).save()
    await message.answer("Токен добавлен")


@router.message(Command("admin"))
async def cmd_add_admin(message: Message, bot: Bot, command: CommandObject):
    try:
        await bot.get_chat(chat_id=int(command.args))
    except TelegramBadRequest:
        await message.answer("Пользователь еще не активировал бота, не могу выдать доступ")
        return
    await Admin(id_tg=command.args).save()
    await message.answer("Админ добавлен")


@router.message(Command("token_del"))
async def cmd_del_token(message: Message, command: CommandObject) -> None:
    token_db = await BitrixToken.get(value=command.args)
    if token_db:
        await token_db.delete()
    await message.answer('Token удален из базы')


@router.message(Command("admin_del"))
async def cmd_del_admin(message: Message, command: CommandObject) -> None:
    admin = await Admin.get(id_tg=command.args)
    if admin:
        await admin.delete()
    await message.answer('Админ удален из базы')


@router.message(Command("help"))
@router.message(F.text == MAIN_BUTTONS.HELP)
async def help(message: Message):
    await message.answer("""
/token {token} - добавить токен битрикс
/token_del {token} - удалить токен битрикс
/admin {id} - добавить админа
/admin_del {id} - удалить админа""")