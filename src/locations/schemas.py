from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class Location(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    longitude: Decimal
    latitude: Decimal
