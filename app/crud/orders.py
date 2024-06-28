from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseCRUD
from app.models.order import Order, OrderCreate
from app.models.user import User


class OrderCRUD(BaseCRUD[Order, OrderCreate, any]):
    async def get(self, db_session: AsyncSession) -> List[Order]:
        statement = select(Order)
        result = await db_session.execute(statement)
        orders = result.scalars().all()
        return orders

    async def retrieve(
        self, unique_id: int, db_session: AsyncSession
    ) -> List[Order]:
        statement = select(Order).where(Order.customer == unique_id)
        result = await db_session.execute(statement)
        orders = result.scalars().all()
        return orders

    async def create(
        self, order: OrderCreate, db_session: AsyncSession
    ) -> Order:
        try:
            db_order = Order(**order.dict())
            db_session.add(db_order)
            await db_session.commit()
            await db_session.refresh(db_order)
            return db_order
        except Exception:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create order",
            )

    async def update(self, unique_id: int, db_session: AsyncSession) -> Order:
        order = await db_session.get(Order, unique_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        order.is_paid = True
        await db_session.commit()
        await db_session.refresh(order)
        return order

    async def delete(
        self, user: User, order_id: int, db_session: AsyncSession
    ) -> HTTPException:
        order = await db_session.get(Order, order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        if order.customer != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )

        await db_session.delete(order)
        await db_session.commit()

        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Order deleted"
        )
