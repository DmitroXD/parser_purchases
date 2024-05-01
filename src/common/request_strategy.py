from abc import ABC, abstractmethod
from typing import Coroutine

from aiohttp import ClientSession, ClientResponse, TCPConnector
from yarl import URL

from core.config import settings
from core.typed import MethodRequest


class AbstractRequestStrategy(ABC):
    def __init__(self, *args, **kwargs):
        self._session = None
        self._args = args
        self._kwargs = kwargs

    def __del__(self):
        if self._session:
            self._session.connector.close()

    def get_cookies(self, url: str):
        return self.session.cookie_jar.filter_cookies(URL(url))

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self._session = self._create_session()
        return self._session

    @abstractmethod
    def _create_session(self) -> ClientSession:
        ...

    @abstractmethod
    def request(self, method: MethodRequest, url: str, *args, **kwargs) -> Coroutine[None, None, ClientResponse]:
        ...

    @abstractmethod
    async def text(self, method: MethodRequest, url: str, *args, **kwargs) -> str:
        ...

    @abstractmethod
    async def json(self, method: MethodRequest, url: str, *args, **kwargs) -> dict | list:
        ...

    @abstractmethod
    async def bytes(self, method: MethodRequest, url: str, *args, **kwargs) -> bytes:
        ...


class BaseRequestStrategy(AbstractRequestStrategy):

    def _create_session(self) -> ClientSession:
        connector = TCPConnector(ttl_dns_cache=200, limit=10)
        return ClientSession(connector=connector, *self._args, **self._kwargs)

    def request(self, method: MethodRequest, url: str, **kwargs) -> Coroutine[None, None, ClientResponse]:
        return self.session.request(method, url, **kwargs)

    async def text(self, method: MethodRequest, url: str, **kwargs) -> str:
        return await (await self.request(method, url, **kwargs)).text(encoding=settings.ENCODING)

    async def json(self, method: MethodRequest, url: str, **kwargs) -> list | dict:
        return await (await self.request(method, url, **kwargs)).json(encoding=settings.ENCODING)

    async def bytes(self, method: MethodRequest, url: str, **kwargs) -> bytes:
        return await (await self.request(method, url, **kwargs)).read()
