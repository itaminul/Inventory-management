from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.customer.models import Customer
    from app.modules.requisition.models import RequisitionItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_code: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    product_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    product_description: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    manufacturer_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    product_price: Mapped[float] = mapped_column(Float, nullable=True)
    product_image: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB, nullable=False, unique=False, default=list
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=True
    )
    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="products",
    )

    requisition_items: Mapped[List["RequisitionItem"]] = relationship(
        "RequisitionItem",
        back_populates="product",
    )
