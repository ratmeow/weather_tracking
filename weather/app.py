from weather.users.routes import router as user_router
from weather.locations.routes import router as location_router
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from weather.settings import DatabaseSettings, WeatherClientSettings
from weather.database import Database
from weather.exceptions import UnauthorizedUserError, UniqueError
import aiohttp
from contextlib import asynccontextmanager
from weather.http_client.implementations import AiohttpClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_settings = DatabaseSettings()
    database = Database(db_settings.db_url)

    app.state.db_settings = db_settings

    app.state.weather_api_settings = WeatherClientSettings()
    app.state.database = database

    app.state.http_client = AiohttpClient(timeout=10.0)
    yield

    await app.state.http_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(location_router)


@app.exception_handler(UnauthorizedUserError)
async def unauthorized_exception_handler(
        request: Request, exc: UnauthorizedUserError
):
    return JSONResponse(status_code=401, content={"message": exc.message})


@app.exception_handler(UniqueError)
async def already_exists_exception_handler(
        request: Request, exc: UniqueError
):
    return JSONResponse(status_code=409, content={"message": exc.message})
