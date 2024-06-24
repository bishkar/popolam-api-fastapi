from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import update
from fastapi import HTTPException

from app.models import Product, ProductCreate, ProductUpdate
from app.crud.base import BaseCRUD


class ProductsCRUD(BaseCRUD[Product, ProductCreate, ProductUpdate]):
    async def get(self, db_session: AsyncSession) -> List[Product]:
        statement = select(Product)
        result = await db_session.execute(statement)
        return result.scalars().all()
        
    async def retrieve(self, unique_id: int, db_session: AsyncSession) -> Product:
        statement = select(Product).where(Product.id == unique_id)
        result = await db_session.execute(statement)
        return result.scalars().first()
        
    async def create(self, data: ProductCreate, db_session: AsyncSession, is_exist: bool) -> Product:
        if is_exist:
            raise HTTPException(status_code=404, detail="Product already exists")
        
        product = Product(**data.dict())
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product) 
        return product

    async def update(self, unique_id: int, data: ProductUpdate, db_session: AsyncSession, is_exist: bool) -> Product:
        if not is_exist:
            raise HTTPException(status_code=404, detail="Product not found")
        
        check_statement = select(Product).where(Product.name == data.name)
        check_result = await db_session.execute(check_statement)
        check_product = check_result.scalars().first()
        if check_product:
            raise HTTPException(status_code=404, detail="Product already exists")

        update_data = data.dict(exclude={'id'})  
        statement = (
            update(Product)
            .where(Product.id == unique_id)
            .values(**update_data)
            .returning(Product)
        )
        
        result = await db_session.execute(statement)
        
        await db_session.commit()
        return HTTPException(status_code=204, detail="Product updated")

    
    async def delete(self, unique_id: int, db_session: AsyncSession, is_exist: bool) -> None:
        if not is_exist:
            raise HTTPException(status_code=404, detail="Product not found")
        
        statement = select(Product).where(Product.id == unique_id)
        result = await db_session.execute(statement)
        product = result.scalars().first()
        await db_session.delete(product)
        await db_session.commit()
        return HTTPException(status_code=204, detail="Product deleted")
    