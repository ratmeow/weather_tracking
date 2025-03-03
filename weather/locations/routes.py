from fastapi import APIRouter, Response, Cookie, Form, HTTPException, Request
from typing import Annotated, Optional
from weather.locations.service import LocationService
from weather.locations.schemas import Location

router = APIRouter(tags=["locations"])


@router.get("/locations")
async def locations_api(session_id: Annotated[Optional[str], Cookie()] = None):
    if session_id:
        return await LocationService.get_locations_by_user_service(session_id=session_id)
    else:
        raise HTTPException(status_code=401)


@router.get("/search")
async def location_search_api(location_name: str,
                              session_id: Annotated[Optional[str], Cookie()] = None):
    locations = await LocationService.search_locations_service(location_name=location_name,
                                                               session_id=session_id)
    return locations


@router.post("/search")
async def location_add_api(location_data: Location,
                           session_id: Annotated[Optional[str], Cookie()] = None):
    await LocationService.add_location_service(location_data=location_data,
                                               session_id=session_id)


@router.delete("/")
async def location_delete_api(location_data: Location,
                              session_id: Annotated[Optional[str], Cookie()] = None):
    await LocationService.delete_location_service(location_data=location_data,
                                                  session_id=session_id)

