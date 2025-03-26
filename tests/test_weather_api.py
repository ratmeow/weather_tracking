import pytest
from decimal import Decimal
from weather.weather_client.open_weather_client import OpenWeatherClient
from weather.http_client.exceptions import AsyncClientInternalError
from weather.weather_client.exceptions import OpenWeatherClientError


@pytest.fixture(scope="module")
def weather_service(mock_http_client, open_weather_settings):
    return OpenWeatherClient(async_client=mock_http_client,
                             settings=open_weather_settings)


@pytest.mark.asyncio
async def test_search_location(weather_service):
    location_name = "Moscow"
    locations = await weather_service.search_location(location_name=location_name)

    assert len(locations) > 0
    assert "Moscow" in [loc.name for loc in locations]
    assert "Kazan" not in [loc.name for loc in locations]


@pytest.mark.asyncio
async def test_search_empty_location(weather_service):
    location_name = ""
    with pytest.raises(AsyncClientInternalError):
        await weather_service.search_location(location_name=location_name)


@pytest.mark.asyncio
async def test_search_location_open_weather_client_error(weather_service):
    location_name = "Ufa"
    with pytest.raises(OpenWeatherClientError):
        await weather_service.search_location(location_name=location_name)


@pytest.mark.asyncio
async def test_get_weather(weather_service):
    lat, lon = Decimal(40), Decimal(60)
    weather = await weather_service.get_weather_by_location(latitude=lat,
                                                            longitude=lon)

    assert weather.latitude == lat
    assert weather.longitude == lon
    assert weather.temperature is not None


@pytest.mark.asyncio
async def test_get_weather_invalid_params(weather_service):
    lat, lon = Decimal(-40), Decimal(60)
    with pytest.raises(AsyncClientInternalError):
        await weather_service.get_weather_by_location(latitude=lat,
                                                      longitude=lon)


@pytest.mark.asyncio
async def test_get_weather_client_error(weather_service):
    lat = lon = Decimal(60)
    with pytest.raises(OpenWeatherClientError):
        await weather_service.get_weather_by_location(latitude=lat,
                                                      longitude=lon)
