from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

class RequisitionItemCreate(BaseModel):
    item_id: int
    quantity: int

class RequisitionItemRead(BaseModel):
    id: int
    item_id: int
    quantity: int
    model_config = ConfigDict(from_attributes=True)

class RequisitionCreate(BaseModel):
    req_number: str
    requested_by: str
    items: List[RequisitionItemCreate]

class RequisitionRead(BaseModel):
    id: int
    req_number: str
    requested_by: str
    status: str
    created_at: datetime
    items: List[RequisitionItemRead]
    model_config = ConfigDict(from_attributes=True)
