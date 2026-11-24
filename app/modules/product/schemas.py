from datetime import datetime
from typing import Annotated, List, Optional

from fastapi.openapi.models import Schema
from pydantic import BaseModel, ConfigDict, PlainSerializer

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

class UpdateProduct(BaseModel):
    product_name: str
    product_description: str
    product_code: str
    customer_id: int
    manufacturer_date: CustomTimestamp


class ProductResponse(BaseModel):
    id: int
    product_name: str
    product_description: str
    product_code: str
    manufacturer_date: CustomTimestamp
    customer_id: int
    customer: Optional[CustomerInfo] = None
    #product_price: float
    # product_quantity: int
    # product_image_url: str
    # product_image_caption: str
    # product_image_caption_image_url: str
    model_config = ConfigDict(from_attributes=True)
