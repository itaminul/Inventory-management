from fastapi import APIRouter
from app.modules.customers.router import router as customer_router

api_router = APIRouter()
api_router.include_router(customer_router, prefix="/customer", tags=["customer"])