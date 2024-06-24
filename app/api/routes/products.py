from fastapi import Depends, APIRouter
from typing import Optional

router = APIRouter()


from app.crud.products import ProductsCRUD
from app.models import Product
from app.dependencies import get_db, object_exists


@router.get("/products/{unique_id}")
async def get_product(unique_id: int, db_session = Depends(get_db)) -> Optional[Product]:
    crud = ProductsCRUD()
    return await crud.retrieve(unique_id, db_session)

@router.get("/products")
async def get_products(db_session = Depends(get_db)) -> list[Product]:
    crud = ProductsCRUD()
    return await crud.get(db_session)

@router.post("/products")
async def create_product(product: Product, db_session = Depends(get_db)) -> Product:
    crud = ProductsCRUD()
    return await crud.create(product, db_session)

@router.put("/products/{unique_id}")
async def update_product(
    unique_id: int,
    product: Product,
    db_session=Depends(get_db),
    is_exist=Depends(object_exists)
) -> None:
    crud = ProductsCRUD()
    return await crud.update(unique_id, product, db_session, is_exist)

@router.delete("/products/{unique_id}")
async def delete_product(
    unique_id: int, 
    db_session=Depends(get_db), 
    is_exist=Depends(object_exists)
) -> None:
    crud = ProductsCRUD()
    return await crud.delete(unique_id, db_session, is_exist)
