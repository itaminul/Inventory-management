from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Table, Integer, String, Boolean, DateTime, ForeignKey, func, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.customer_type.models import CustomerType
    from app.modules.product.models import Product


    # 1. Define this BEFORE class Customer (remove it from product/models.py if it's also there)
customer_products = Table(
        "customer_products",
        Base.metadata,
        Column("customer_id", ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
        Column("product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    )

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_code = Column(String, unique=False, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    customer_type_id: Mapped[int] = mapped_column(
        ForeignKey("customer_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    customer_type: Mapped["CustomerType"] = relationship(
        "CustomerType",
        back_populates="customers",
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="customer",
    )
