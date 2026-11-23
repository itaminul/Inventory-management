from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.customer.schemas import CustomerCreate , CustomerUpdate

from app.modules.customer.repository import CustomerRepository

class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def get_customer(self, customer_id: int):
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        return customer

    def list_customers(self):
        return self.repository.get_all()

    def create_customer(self, customer_data: CustomerCreate):
        if self.repository.get_by_email(customer_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        return self.repository.create(customer_data)

    def update_customer(self, customer_id: int, customer_data: CustomerUpdate):
        existing_customer = self.repository.get_by_id(customer_id)
        if not existing_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        if customer_data.email and customer_data.email != existing_customer.email:
            email_owner = self.repository.get_by_email(customer_data.email)
            if email_owner:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Must be outside the 'if' block so updating 'name' alone still saves!
        return self.repository.update(existing_customer, customer_data)

    def delete_customer(self, customer_id: int):
        existing_customer = self.repository.get_by_id(customer_id)
        if not existing_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        self.repository.delete(existing_customer)