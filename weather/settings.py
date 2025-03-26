from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os


def get_env_path():
    if os.getenv("APP_MODE", "prod") == "test":
        return os.path.join(os.path.dirname(__file__), "..", "tests", ".env")
    return os.path.join(os.path.dirname(__file__), "..", ".env")


class WeatherClientSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_path(), extra="ignore")

    API_KEY: str = Field(validation_alias="OPENWEATHER_API_KEY")
    SEARCH_URL: str = Field(validation_alias="OPENWEATHER_SEARCH_URL")
    WEATHER_URL: str = Field(validation_alias="OPENWEATHER_WEATHER_URL")


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_path(), extra="ignore")

    PG_USER: str = Field(validation_alias="POSTGRES_USER")
    PG_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    PG_DB: str = Field(validation_alias="POSTGRES_DB")
    PG_HOST: str = Field(validation_alias="POSTGRES_HOST")
    PG_PORT: str = Field(validation_alias="POSTGRES_OUTER_PORT")

    @property
    def db_url(self):
        return f"""postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"""
