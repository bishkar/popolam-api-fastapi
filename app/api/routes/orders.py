from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import get_current_user
from app.crud.orders import OrderCRUD
from app.dependencies import get_db
from app.models import Order, OrderCreate
from app.models.user import User

router = APIRouter()


@router.get("/{user_id}")
async def get_user_orders(
    user_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> List[Order]:
    if not user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource",
        )
    crud = OrderCRUD()

    return await crud.retrieve(user_id, db_session)


@router.get("/")
async def get_all_orders(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[Order]:
    if not user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource",
        )

    crud = OrderCRUD()
    return await crud.get(db_session)


@router.post("/")
async def make_order(
    order: OrderCreate,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Order:
    crud = OrderCRUD()
    order.customer = user.id
    return await crud.create(order, db_session)


@router.put("/{order_id}")
async def close_order(
    order_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Order:
    crud = OrderCRUD()
    if not user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource",
        )

    return await crud.update(order_id, db_session)


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    crud = OrderCRUD()

    return await crud.delete(user, order_id, db_session)
