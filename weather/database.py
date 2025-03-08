from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from weather.exceptions import DatabaseInternalError
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(url=self.db_url)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)


async def get_session(database: Database):
    async with database.async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database Error: ", e)
            raise DatabaseInternalError
        finally:
            await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
