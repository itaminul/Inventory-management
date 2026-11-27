from datetime import datetime
from typing import Annotated, List, Optional

from fastapi.openapi.models import Schema
from pydantic import BaseModel, ConfigDict, PlainSerializer, field_validator
from sqlalchemy.orm import Any
CustomTimestamp = Annotated[
    datetime,
    PlainSerializer(lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"), return_type=str),
]
class CustomerInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_code: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class ProductCreate(BaseModel):
    product_name: str
    product_description: str
    product_code: str
    customer_id: int
    manufacturer_date: CustomTimestamp
    product_image: dict[str, Any] | None = None

class UpdateProduct(BaseModel):
    product_name: str
    product_description: str
    product_code: str
    product_price: float
    product_image: str
    customer_id: int
    manufacturer_date: CustomTimestamp


class ProductResponse(BaseModel):
    id: int
    product_name: str
    product_description: str
    product_code: str
    manufacturer_date: CustomTimestamp
    product_price: float
    # product_quantity: int
    product_image: dict[str, Any] | None = None
    # product_image_caption: str
    # product_image_caption_image_url: str
    @field_validator("product_price", mode="before")
    @classmethod
    def default_price_if_none(cls, value: float | None) -> float:
        return 0.0 if value is None else value
    customer_id: int
    customer: Optional[CustomerInfo] = None
    model_config = ConfigDict(from_attributes=True)
