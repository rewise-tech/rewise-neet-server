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


# MockTest Schemas
class MockTestBase(BaseModel):
    marks_scored: Optional[int] = 0
    negative_marks: Optional[int] = 0
    test_status: str
    questions: Optional[dict] = None
    time_taken: Optional[int] = 0
    user_id: int


class MockTestCreate(MockTestBase):
    pass


class MockTestUpdate(BaseModel):
    marks_scored: Optional[int] = None
    negative_marks: Optional[int] = None
    test_status: Optional[str] = None
    questions: Optional[dict] = None
    time_taken: Optional[int] = None


class MockTestRead(MockTestBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
