from sqlalchemy.orm import Session

from app.modules.customers.models import Customer


def create_customer(
    db: Session,
    customer_data: dict,
) -> Customer:

    customer = Customer(**customer_data)

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers(db: Session):

    return db.query(Customer).all()


def get_customer(
    db: Session,
    customer_id: int,
):

    return db.query(Customer).filter(
        Customer.id == customer_id
    ).first()