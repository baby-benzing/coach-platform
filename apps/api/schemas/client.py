from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None


class ClientResponse(BaseModel):
    id: str
    coach_id: str
    name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
