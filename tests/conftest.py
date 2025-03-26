import pytest

from weather.settings import WeatherClientSettings
from tests.http_client_mock import MockAsyncHTTPClient

pytest_plugins = ['pytest_asyncio']


@pytest.fixture(scope="module")
def open_weather_settings():
    return WeatherClientSettings()


@pytest.fixture(scope="module")
def mock_http_client():
    return MockAsyncHTTPClient()



