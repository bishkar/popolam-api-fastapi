from fastapi import APIRouter

from app.api.routes import basic, products

api_router = APIRouter()

api_router.include_router(basic.router, tags=["basic"])
api_router.include_router(products.router, prefix="/products", tags=["products"])