import aiohttp
from yarl import URL

from common.open_api.abstract_api import AbstractAPI
from core.config import settings
from core.typed import MethodRequest


class RusProfile(AbstractAPI):
    __base_url = 'https://www.rusprofile.ru'
    __auth_url = '/auth.php?action=login'
    __search = '/search'

    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password
        super().__init__(
            base_url=self.__base_url,
            headers={
                "User-Agent": settings.USER_AGENT,
                "Host": "www.rusprofile.ru",
                "Origin": "https://www.rusprofile.ru"
            }
        )

    @property
    def session_id(self):
        return self.request.session.cookie_jar.filter_cookies(URL(self.__base_url)).get("sessid").value

    async def call_method(self, method: MethodRequest, url: str, **kwargs):
        if not self.session_id:
            await self._auth()
        response = await self.request.json(method, url, **kwargs)
        if response["message"] == "OK":
            return response
        raise Exception(response)

    async def _auth(self):
        await self.request.text("GET", "/")
        csrf = self.request.get_cookies(self.__base_url).get("__Host-csrf-token").value
        return await self.request.json("POST", self.__auth_url, data={
            "login": self._login,
            "password": self._password,
            'switch': True
        }, headers={
            "X-Csrf-Token": csrf
        })


base_rusprofile = RusProfile(settings.RUS_PROFILE_LOGIN, settings.RUS_PROFILE_PASSWORD)


class RusProfile(AbstractAPI):
    __base_url = 'https://www.rusprofile.ru'

    __auth_url = '/auth.php?action=login'
    __search = '/search'

    async def __request(self, *args, **kwargs):
        async with aiohttp.ClientSession(base_url=self.__base_url, **self.request_kwargs) as session:
            async with session.request(*args, **kwargs) as response:
                html = await response.text()
                return html

    async def search_participant(self, query: str, search_inactive: bool = False):
        response = await self.__request('get', self.__search, params={
            'query': query,
            'search_inactive': int(search_inactive)
        })
        return response
