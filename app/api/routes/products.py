from fastapi import Depends, APIRouter, HTTPException, Request
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from app.api.routes.auth import get_current_user
from app.crud.products import ProductsCRUD
from app.models import Product, ProductCreate, ProductUpdate
from app.dependencies import get_db
from app.misc import ProductChecker, ObjectChecker
from app.models.user import User


router = APIRouter()

@router.get("/{unique_id}")
async def get_product(
    unique_id: int, 
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[Product]:
    crud = ProductsCRUD()
    return await crud.retrieve(unique_id, db_session)

@router.get("/")
@cache(expire=60, namespace="products")
async def get_products(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> list[Product]:
    crud = ProductsCRUD()
    return await crud.get(db_session)

@router.post("/")
async def create_product(
    product: ProductCreate,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Product:
    crud = ProductsCRUD()
    ObjectChecker.set_checker(ProductChecker)

    if not user.is_staff:
        raise HTTPException(status_code=403, detail="You are not allowed to perform this action")

    is_exist = await ObjectChecker.check(request)
    return await crud.create(product, db_session, is_exist)

@router.put("/{unique_id}")
async def update_product(
    unique_id: int,
    product: ProductUpdate,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    crud = ProductsCRUD()
    ObjectChecker.set_checker(ProductChecker)

    if not user.is_staff:
        raise HTTPException(status_code=403, detail="You are not allowed to perform this action")

    is_exist = await ObjectChecker.check(request)
    return await crud.update(unique_id, product, db_session, is_exist)

@router.delete("/{unique_id}")
async def delete_product(
    unique_id: int, 
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    crud = ProductsCRUD()
    ObjectChecker.set_checker(ProductChecker)

    if not user.is_staff:
        raise HTTPException(status_code=403, detail="You are not allowed to perform this action")
    
    is_exist = await ObjectChecker.check(request)
    return await crud.delete(unique_id, db_session, is_exist)
