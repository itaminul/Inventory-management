from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.customer.models import Customer

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_code: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    product_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    product_description: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    manufacturer_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=True
    )
    customer: Mapped["Customer"] = relationship(
         "Customer",
         back_populates="products"
    )



