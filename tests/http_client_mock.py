from typing import Optional
import random
from weather.http_client.exceptions import AsyncClientInternalError

from weather.http_client.base import AsyncHTTPClient


class MockAsyncHTTPClient(AsyncHTTPClient):
    async def get(self, url: str, params: Optional[dict]) -> dict | list[dict]:
        if "location" in url:
            if len(params["q"]) == 0:
                raise AsyncClientInternalError
            if "Ufa" in params["q"]:
                return [{"name_": params["q"],
                         "lat": random.random() * 100,
                         "lon": random.random() * 100} for i in range(random.randint(1, 5))]
            return [{"name": params["q"],
                     "lat": random.random() * 100,
                     "lon": random.random() * 100} for i in range(random.randint(1, 5))]

        if "weather" in url:
            if params["lat"] < 0 or params["lon"] < 0:
                raise AsyncClientInternalError
            if params["lat"] == params["lon"]:
                return [{}]
            return {"main": {"temp": 10}}

    async def close(self):
        pass
