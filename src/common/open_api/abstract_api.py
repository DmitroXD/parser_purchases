from abc import ABC, abstractmethod

from common.base_request import BaseRequest
from core.typed import MethodRequest


class AbstractAPI(BaseRequest, ABC):
    @abstractmethod
    def call_method(self, method: MethodRequest, url: str, **kwargs):
        ...
