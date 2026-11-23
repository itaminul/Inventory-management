from fastapi import HTTPException, status
from http.client import HTTPException

from sqlalchemy.orm import Session

from app.modules.customers import repository
from app.modules.customers.models import Customer
from app.modules.customers.schemas import (
CustomerCreate,
CustomerUpdate,
)

def create_customer(
        db: Session,
        customer_data: CustomerCreate,
):
    return repository.create_customer(
        db,
        customer_data.model_dump()
    )
def get_customer(db: Session, customer_id: int):
    return repository.get_customers(db)

def update_customer(
        db: Session,
        customer_id: int,
        customer_data: CustomerUpdate,
):
    customer = get_customer(db, customer_id)
    update_data = customer_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The customer with that id was not found."
        )

        return repository.update_customer(
            db,
            customer,
            customer_data.model_dump()
        )