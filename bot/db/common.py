from sqlalchemy.orm import sessionmaker

from bot.db.base import BaseModel


async def merge(model: BaseModel, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.merge(model)
