from abc import ABC, abstractmethod


class WeatherClient(ABC):

    @abstractmethod
    async def search_location(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_weather_by_location(self, *args, **kwargs):
        pass
