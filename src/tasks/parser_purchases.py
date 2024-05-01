import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from bitrix24 import BitrixError
from bs4 import BeautifulSoup

from common.open_api.bitrix24 import Bitrix
from common.open_api.purchases import base_purchases
from core.config import settings
from database.models import Participant, BitrixToken
from tools.awaitable import run_async_forever


async def main():
    logging.info('START PARSER PURCHASES')
    await run_async_forever(loops, timeout=10)


async def loops():
    new_participants = await base_purchases.get_new_participants(check=30)
    info = await get_info_about_new_participants(new_participants)
    for i in info:
        soup, number = i
        data = await asyncio.to_thread(check_info, soup)
        if not await Participant.exists(number=number):
            await send_all_bitrix(number=number, **data)


async def get_info_about_new_participants(numbers: list[str]):
    info_pages_async = [base_purchases.get_info_participant(number) for number in numbers]
    return await asyncio.gather(*info_pages_async)


def check_info(soup: BeautifulSoup):
    def format_info(_info: str) -> str:
        return _info.replace("\n", "").strip()

    contact_info = get_block_by_title(soup, "Контактная информация")
    contact_data = {}
    for i in contact_info.find_all(class_="blockInfo__section section"):
        now, info = i.find_all("span")
        now, info = now.text, info.text
        if now not in contact_data:
            contact_data[now] = info.replace("\n", "")
    purchase_info = get_block_by_title(soup, "Информация об объекте закупки").find("tbody")
    purchase_info = purchase_info.find("tr", {"class": "tableBlock__row"}).find_all(class_="tableBlock__col")
    purchase_data = {
        "НАИМЕНОВАНИЕ ТОВАРА, РАБОТЫ, УСЛУГИ": purchase_info[2].text,
        "Количество": format_info(purchase_info[4].text),
        "Цена за ед.": format_info(purchase_info[5].text).replace(" ", ""),
        "Стоимость": format_info(purchase_info[6].text).replace(" ", ""),
    }
    contact_data.update(purchase_data)
    return contact_data


def get_block_by_title(soup: BeautifulSoup, title: str):
    return soup.find(
        "h2",
        {"class": "blockInfo__title"},
        text=lambda x: title in x
    ).parent


async def send_all_bitrix(number: str, **data):
    tokens: list[BitrixToken] = await BitrixToken.all()
    if tokens:
        await Participant(number=number).save()
        for obj in tokens:
            try:
                bitrix = Bitrix(obj.value)
                await asyncio.to_thread(bitrix.add_lead(**data))
            except BitrixError:
                await obj.delete()
                bot: Bot = Bot(token=settings.BOT_TOKEN)
                try:
                    await bot.send_message(
                        chat_id=settings.ADMINISTRATOR_ID,
                        text=f"Не удалось добавить лид в Bitrix. Проверьте токен: <code>{obj.value}</code>"
                    )
                except TelegramBadRequest:
                    ...
