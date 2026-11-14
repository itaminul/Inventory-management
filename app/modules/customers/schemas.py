from pydantic import BaseModel, ConfigDict, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool | None = None
class CustomerUpdate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool = True

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr | None
    phone: str | None
    address: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)