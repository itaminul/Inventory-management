from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Ensure all models are always registered with Base.metadata
from app.modules.customer.models import Customer  # noqa: E402, F401
from app.modules.customer_type.models import CustomerType  # noqa: E402, F401
from app.modules.product.models import Product  # noqa: E402, F401
from app.modules.requisition.models import Requisition, RequisitionItem 