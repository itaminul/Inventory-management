from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.customer.router import router as customer_router
from app.modules.product.router import router as product_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(customer_router, prefix="/customer", tags=["customer"])
api_router.include_router(product_router, prefix="/product", tags=["product"])
