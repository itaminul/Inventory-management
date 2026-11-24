from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
class CustomerTypeInfo(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class CustomerCreate(BaseModel):
    customer_code: str
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    customer_type_id: int = Field(..., description="ID of the customer type")
    is_active: bool = Field(default=True, description="Indicates whether the customer is active or not")


class CustomerUpdate(BaseModel):
    customer_code: str
    name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    customer_type_id: int | None = None
    is_active: bool | None = None


class CustomerResponse(BaseModel):
    id: int
    customer_code: str
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    customer_type_id: int
    customer_type: CustomerTypeInfo | None = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
