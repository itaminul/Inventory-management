from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

class UserRegister(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    
class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str | None = None
    email: EmailStr | None = None
    password: str

    @model_validator(mode="after")
    def require_login_identifier(self) -> Self:
        if self.username is None and self.email is None:
            raise ValueError("Either username or email is required")
        return self
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    
class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str = "bearer"            