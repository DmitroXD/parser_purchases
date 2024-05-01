import re

from common.open_api.abstract_api import AbstractAPI
from core.config import settings
from core.typed import MethodRequest
from bs4 import BeautifulSoup

from database.models.participant import Participant


class Purchases(AbstractAPI):
    __base_url = 'https://zakupki.gov.ru'

    new_participant = '/epz/order/extendedsearch/results.html'
    info_participant = '/epz/order/notice/ok20/view/common-info.html'

    def __init__(self):
        super().__init__(
            base_url=self.__base_url,
            headers={
                "User-Agent": settings.USER_AGENT,
                "Host": "zakupki.gov.ru",
                "doNotAdviseToChangeLocationWhenIosReject": "true",
                "Accept-Encoding": "gzip, deflate, br"
            })

    async def call_method(self, method: MethodRequest, url: str, **kwargs):
        response = await self.request.text(method=method, url=url, **kwargs)
        return BeautifulSoup(response, 'html.parser')

    async def get_new_participants(self, num: int = 1, check: int = 50) -> list[str]:
        soup = await self.call_method('GET', self.new_participant, params={
            'pageNumber': num,
            'recordsPerPage': check,
            "search-filter": "Дате+размещения",
            "sortDirection": "false",
            "sortBy": "UPDATE_DATE",
            "fz44": "on",
            "fz223": "on",
            "af": "on",
            "currencyIdGeneral": -1
        })
        all_tags = soup.find_all(
            'a',
            {'target': '_blank', 'href': re.compile(r"\?regNumber=(\d+)")},
            text=True
        )
        all_numbers = set([tag['href'].split('=')[1] for tag in all_tags])
        return [num for num in all_numbers if num and not await Participant.exists(number=num)]

    async def get_info_participant(self, number: int | str) -> tuple[BeautifulSoup | None, str]:
        response = await self.call_method('GET', self.info_participant, params={
            'regNumber': number
        })
        status = response.find("div", {"class": "cardMainInfo__status"})
        if not status or "подача заявок" not in status.text.strip().lower():
            return None, number
        return response, number


base_purchases = Purchases()
