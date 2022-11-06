from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def get_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=True,
        encoding='utf-8',
    )


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
