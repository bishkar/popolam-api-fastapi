from fastapi import APIRouter

from app.api.routes import basic, products, user, auth, orders

api_router = APIRouter()

api_router.include_router(basic.router, tags=["basic"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/token", tags=["auth"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])