import pytest
from weather.locations.open_weather_service import OpenWeatherAPI
from weather.settings import WeatherAPISettings
import pytest_asyncio
from tests.http_client_mock import MockAsyncHTTPClient

pytest_plugins = ['pytest_asyncio']


@pytest.fixture(scope="module")
def open_weather_settings():
    return WeatherAPISettings()


@pytest_asyncio.fixture()
def mock_http_client():
    return MockAsyncHTTPClient()


@pytest_asyncio.fixture()
def open_weather_api(mock_http_client, open_weather_settings):
    return OpenWeatherAPI(async_client=mock_http_client,
                          settings=open_weather_settings)
