import uuid
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.customer.schemas import CustomerCreate, CustomerUpdate
from app.modules.customer.service import CustomerService
from app.modules.customer.schemas import CustomerResponse
router = APIRouter()

@router.get("/", response_model=list[CustomerResponse])
def read_customers(db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.list_customers()

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.create_customer(customer)

@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
        customer_id: int,
        customer: CustomerUpdate,
        db: Session = Depends(get_db),

):
    service = CustomerService(db)
    updated_customer = service.update_customer(customer_id, customer)
    return updated_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
        customer_id: int,
        db: Session = Depends(get_db),
):
    service = CustomerService(db)
    service.delete_customer(customer_id)
    return None