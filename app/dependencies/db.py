from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends

from app.database import async_session
from app.models import Product


# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         yield session

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    print(request.state)
    async with async_session() as session:
        request.state.db = session
        yield session


async def object_exists(request: Request) -> bool:
    statement = select(Product).where(Product.id == int(request.path_params['unique_id']))
    result = await request.state.db.execute(statement)
    product = result.scalars().first()
    return product is not None
