from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from typing import List
from sqlalchemy import String, DateTime, ForeignKey
from app.modules.product.models import Product

from app.database.base import Base

class Requisition(Base):
    __tablename__ = "requisitions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    req_number: Mapped[str] = mapped_column(String(30), default="pending", unique=False)
    dept_id: Mapped[int] = mapped_column(unique=False)
    request_by: Mapped[int] = mapped_column(unique=False)
    requisition_date: Mapped[int] = mapped_column(DateTime, index=True)
    items: Mapped[List["RequisitionItem"]] = relationship(
        back_populates="requisition",
        cascade="all, delete, delete-orphan",
    )

class RequisitionItem(Base):
    __tablename__ = "requisition_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    requisition_id: Mapped[int] = mapped_column(ForeignKey("requisitions.id"), index=True)
    item_ids: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"))
    request_by: Mapped[int] = mapped_column(index=False)
    quantity: Mapped[int] = mapped_column(index=False)
    unit_price: Mapped[int] = mapped_column(index=False)
    unit: Mapped[int] = mapped_column(index=False)
    requisition: Mapped["Requisition"] = relationship(back_populates="requisition_items")
    products: Mapped["Product"] = relationship(
        back_populates="requisition_items",
    )


