from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH)
    PG_USER: str = Field(validation_alias="POSTGRES_USER")
    PG_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    PG_DB: str = Field(validation_alias="POSTGRES_DB")
    PG_HOST: str = Field(validation_alias="POSTGRES_HOST")
    PG_PORT: str = Field(validation_alias="POSTGRES_OUTER_PORT")

    @property
    def db_url(self):
        return f"""postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"""


db_settings = DatabaseConfig()
