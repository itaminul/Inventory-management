from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Customer
from app.modules.customer.schemas import CustomerCreate, CustomerUpdate


class CustomerRepository:
    
    def __init__(self, db: Session):
        self.db = db
    def get_customers(db: Session):
        repo = CustomerRepository(db)
        return repo.get_all()
    def get_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()
    def get_all(self) -> list[Customer]:
        return (
            self.db.query(Customer)
            .filter(Customer.is_active.is_(True))
            .order_by(Customer.id.asc())
            .all()
        )

    def get_by_email(self, email: str) -> Customer | None:
        return self.db.query(Customer).filter(Customer.email == email).first()

    def create(self, customer_data: CustomerCreate):
        new_customer = Customer(**customer_data.model_dump())
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def update(self, customer: Customer, customer_data: CustomerUpdate):
        update_field = customer_data.model_dump(exclude_unset=True)

        for key, value in update_field.items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer_id: int):
        self.db.delete(customer_id)
        self.db.commit()