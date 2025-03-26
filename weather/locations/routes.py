from fastapi import APIRouter, Response, Cookie, Form, HTTPException, Request, Depends
from weather.locations.service import LocationService
from weather.locations.schemas import LocationDTO, LocationResponse, WeatherResponse
from weather.users.schemas import UserDTO
from weather.dependencies import get_location_service, get_user

router = APIRouter(tags=["locations"])


@router.get("/locations")
async def locations_api(user: UserDTO = Depends(get_user),
                        location_service: LocationService = Depends(get_location_service)) -> list[WeatherResponse]:
    return await location_service.get_locations_by_user(user_id=user.id)


@router.get("/search")
async def location_search_api(location_name: str,
                              location_service: LocationService = Depends(get_location_service)) -> list[LocationResponse]:
    locations = await location_service.search_location(location_name=location_name)
    return locations


@router.post("/search")
async def location_add_api(location_data: LocationDTO,
                           user: UserDTO = Depends(get_user),
                           location_service: LocationService = Depends(get_location_service)):
    await location_service.add_location(location_data=location_data,
                                        user_id=user.id)


@router.delete("/")
async def location_delete_api(location_data: LocationDTO,
                              user: UserDTO = Depends(get_user),
                              location_service: LocationService = Depends(get_location_service)):
    await location_service.delete_location(location_data=location_data,
                                           user_id=user.id)
