from weather.users.routes import router as user_router
from weather.locations.routes import router as location_router
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from weather.settings import DatabaseSettings, AppSettings
from weather.database import Database

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    db_settings = DatabaseSettings()
    database = Database(app.state.db_settings.db_url)

    app.state.db_settings = db_settings
    app.state.app_settings = AppSettings()
    app.state.database = database


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(location_router)
