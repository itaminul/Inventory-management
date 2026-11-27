from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.product.models import Product


class Requisition(Base):
    __tablename__ = "requisitions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    req_number: Mapped[str] = mapped_column(String(30), default="pending", unique=False)
    dept_id: Mapped[int] = mapped_column(unique=False)
    request_by: Mapped[int] = mapped_column(unique=False)
    requisition_date: Mapped[datetime] = mapped_column(DateTime, index=True)

    items: Mapped[List["RequisitionItem"]] = relationship(
        "RequisitionItem",
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

    requisition: Mapped["Requisition"] = relationship(
        "Requisition",
        back_populates="items",
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="requisition_items",
    )
