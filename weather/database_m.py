from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from weather.config import db_settings
from weather.exceptions import DatabaseInternalError
import logging
import asyncpg

logger = logging.getLogger(__name__)


class SessionCreator:
    def __init__(self, db_url):
        self.engine = create_async_engine(url=db_url)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self):
        async with self.async_session_maker() as session:
            yield session


def connection(commit: bool = False):
    def decorator(method):
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    result = await method(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except asyncpg.exceptions.UniqueViolationError as e:
                    logger.error("Unique Error: ", e)
                except Exception as e:
                    await session.rollback()
                    logger.error("Database Error: ", e)
                    raise DatabaseInternalError
                finally:
                    await session.close()

        return wrapper

    return decorator


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
