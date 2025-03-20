from typing import Optional

from weather.http_client.base import AsyncHTTPClient

class MockAsyncHTTPClient(AsyncHTTPClient):
    async def get(self, url: str, params: Optional[dict]) -> dict:
        pass

    async def close(self):
        pass