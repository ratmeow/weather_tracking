import pytest
from weather.weather_client.open_weather_client import OpenWeatherClient
from weather.settings import WeatherClientSettings
import pytest_asyncio
from tests.http_client_mock import MockAsyncHTTPClient

pytest_plugins = ['pytest_asyncio']


@pytest.fixture(scope="module")
def open_weather_settings():
    return WeatherClientSettings()


@pytest_asyncio.fixture()
def mock_http_client():
    return MockAsyncHTTPClient()


@pytest_asyncio.fixture()
def open_weather_api(mock_http_client, open_weather_settings):
    return OpenWeatherClient(async_client=mock_http_client,
                             settings=open_weather_settings)
