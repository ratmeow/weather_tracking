from weather.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from uuid import UUID
from datetime import datetime


class UserORM(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class UserSessionORM(Base):
    __tablename__ = "user_sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expired_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user = relationship("UserORM", uselist=False, lazy="joined")
