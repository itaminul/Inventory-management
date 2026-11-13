from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.modules.customers import service
from app.modules.customers.schemas import (
CustomerCreate,
CustomerResponse
)

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
        customer_data: CustomerCreate,
        db: Session = Depends(get_db),
):
    return service.create_customer(
        db,
        customer_data,
    )
@router.get(
    "/",
    response_model=list[CustomerResponse],
    status_code=status.HTTP_200_OK)

def get_customers(
        db: Session = Depends(get_db),
):
    return service.get_customers(db)
