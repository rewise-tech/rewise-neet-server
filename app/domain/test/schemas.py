from typing import Optional

from pydantic import BaseModel, ConfigDict


class TestSettingsBase(BaseModel):
    key: str
    value: str
    is_active: Optional[bool] = True


class TestSettingsCreate(TestSettingsBase):
    pass


class TestSettingsUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None
    is_active: Optional[bool] = None


class TestSettingsRead(TestSettingsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
