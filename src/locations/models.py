from decimal import Decimal
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class LocationModel(Base):
    __tablename__ = "locations"

    name: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[Decimal] = mapped_column(nullable=False)
    longitude: Mapped[Decimal] = mapped_column(nullable=False)


class LocationUserModel(Base):
    __tablename__ = "user_location_relation"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
