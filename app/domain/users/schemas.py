from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    mobile: str = Field(..., max_length=32)
    role: str = Field(default="user", max_length=64)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    mobile: Optional[str] = Field(default=None, max_length=32)
    password: Optional[str] = Field(default=None, min_length=6, max_length=255)
    role: Optional[str] = Field(default=None, max_length=64)
    is_active: Optional[bool] = None


class UserRead(UserBase):
    id: int

    model_config = {"from_attributes": True}
