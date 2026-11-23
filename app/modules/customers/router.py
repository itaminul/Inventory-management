from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.modules.customers import service
from app.modules.customers.schemas import (
CustomerCreate,
CustomerUpdate,
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
    return service.get_customer(db)

    @router.patch("/{customer_id}", response_model=list[CustomerResponse])
    def update_customer(
            customer_id: int,
            customer_data  : CustomerUpdate,
            db: Session = Depends(get_db),
    ):
       return service.update_customer(
           db,
           customer_id,
           customer_data,
       )


