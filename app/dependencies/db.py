from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with async_session as session:
        request.state.db = session
        yield session
