from tests.conftest import open_weather_api
import pytest


@pytest.mark.asyncio
async def test_search_location(open_weather_api):
    weather_service = open_weather_api
    location_name = "Moscow"

    locations = await weather_service.search_location(location_name=location_name)
    assert {"M"}

