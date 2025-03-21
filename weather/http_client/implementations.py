import aiohttp
from typing import Optional

from .base import AsyncHTTPClient
from .exceptions import RemoteServerError


class AiohttpClient(AsyncHTTPClient):
    def __init__(self, timeout: float):
        super().__init__(timeout=timeout)
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout))

    @staticmethod
    def exception_handler(method):
        async def wrapper(self, *args, **kwargs):
            try:
                return await method(self, *args, **kwargs)
            except aiohttp.ClientResponseError:
                raise RemoteServerError

        return wrapper

    @exception_handler
    async def get(self, url: str, params: Optional[dict]) -> dict:
        async with self.session.get(url=url, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def close(self):
        await self.session.close()
