from common.request_strategy import AbstractRequestStrategy, BaseRequestStrategy


class BaseRequest:
    def __init__(self, request_strategy: AbstractRequestStrategy = None, **kwargs):
        self._request = request_strategy or BaseRequestStrategy(**kwargs)

    @property
    def request(self) -> AbstractRequestStrategy:
        return self._request
