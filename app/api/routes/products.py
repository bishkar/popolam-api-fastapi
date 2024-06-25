from fastapi import Depends, APIRouter, Request
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import ObjectChecker
from app.crud.products import ProductsCRUD
from app.models import Product
from app.dependencies import get_db
from app.dependencies import ObjectChecker, ProductChecker


router = APIRouter()

@router.get("/products/{unique_id}")
async def get_product(
    unique_id: int, 
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[Product]:
    crud = ProductsCRUD()
    return await crud.retrieve(unique_id, db_session)

@router.get("/products")
async def get_products(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> list[Product]:
    crud = ProductsCRUD()
    return await crud.get(db_session)

@router.post("/products")
async def create_product(
    product: Product,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> Product:
    crud = ProductsCRUD()
    ObjectChecker.set_checker(ProductChecker)

    is_exist = await ObjectChecker.check(request)
    return await crud.create(product, db_session, is_exist)

@router.put("/products/{unique_id}")
async def update_product(
    unique_id: int,
    product: Product,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    crud = ProductsCRUD()
    ObjectChecker.set_checker(ProductChecker)

    is_exist = await ObjectChecker.check(request)
    return await crud.update(unique_id, product, db_session, is_exist)

@router.delete("/products/{unique_id}")
async def delete_product(
    unique_id: int, 
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    crud = ProductsCRUD()
    ObjectChecker.set_checker(ProductChecker)
    
    is_exist = await ObjectChecker.check(request)
    return await crud.delete(unique_id, db_session, is_exist)
