from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")
    OPENWEATHER_API_KEY: str = Field(validation_alias="OPENWEATHER_API_KEY")


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")
    PG_USER: str = Field(validation_alias="POSTGRES_USER")
    PG_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    PG_DB: str = Field(validation_alias="POSTGRES_DB")
    PG_HOST: str = Field(validation_alias="POSTGRES_HOST")
    PG_PORT: str = Field(validation_alias="POSTGRES_OUTER_PORT")

    @property
    def db_url(self):
        return f"""postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"""


app_settings = AppSettings()
db_settings = DatabaseConfig()
