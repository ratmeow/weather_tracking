from decimal import Decimal
from weather.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class LocationORM(Base):
    __tablename__ = "locations"

    name: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[Decimal] = mapped_column(nullable=False)
    longitude: Mapped[Decimal] = mapped_column(nullable=False)


class LocationUserORM(Base):
    __tablename__ = "user_location_relation"
    id = None
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), primary_key=True)
