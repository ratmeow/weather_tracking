from fastapi import APIRouter, Response, Cookie, Form, HTTPException, Request, Depends
from typing import Annotated, Optional
from weather.locations.service import LocationService
from weather.locations.schemas import Location
from weather.users.schemas import UserSchema
from weather.dependencies import get_location_service, get_user

router = APIRouter(tags=["locations"])


@router.get("/locations")
async def locations_api(user: UserSchema = Depends(get_user),
                        location_service: LocationService = Depends(get_location_service)):
    return await location_service.get_locations_by_user_service(user_id=user.id)


@router.get("/search")
async def location_search_api(location_name: str,
                              location_service: LocationService = Depends(get_location_service)):
    locations = await location_service.search_locations_service(location_name=location_name)
    return locations


@router.post("/search")
async def location_add_api(location_data: Location,
                           user: UserSchema = Depends(get_user),
                           location_service: LocationService = Depends(get_location_service)):
    await location_service.add_location_service(location_data=location_data,
                                                user_id=user.id)


@router.delete("/")
async def location_delete_api(location_data: Location,
                              user: UserSchema = Depends(get_user),
                              location_service: LocationService = Depends(get_location_service)):
    await location_service.delete_location_service(location_data=location_data,
                                                   user_id=user.id)
