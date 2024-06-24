from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import async_session
from app.models import Product, User


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with async_session as session:
        request.state.db = session
        yield session

async def product_exists(request: Request) -> bool:
    match request.method:
        case "POST":
            body = await request.json()
            statement = select(Product).where(Product.name == body.get('name'))
        case "PUT":
            statement = select(Product).where(Product.id == int(request.path_params['unique_id']))
        case "DELETE":
            statement = select(Product).where(Product.id == int(request.path_params['unique_id']))

    result = await request.state.db.execute(statement)
    product = result.scalars().first()
    return product is not None

async def user_exists(request: Request) -> bool:
    match request.method:
        case "POST":
            body = await request.json()
            statement = select(User).where(User.username == body.get('username')
                                           or User.email == body.get('email'))
        case "PUT":
            statement = select(User).where(User.id == int(request.path_params['unique_id']))
        case "DELETE":
            statement = select(User).where(User.id == int(request.path_params['unique_id']))

    result = await request.state.db.execute(statement)
    user = result.scalars().first()
    return user is not None
