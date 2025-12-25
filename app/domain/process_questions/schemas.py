from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Stage Option Schemas ---


class StageOptionBase(BaseModel):
    label: str = Field(..., max_length=50, description="Option label like A, B, C, D")
    text: str = Field(..., description="The text content of the option")
    has_diagram: bool = False
    diagram_description: Optional[str] = None
    diagram_name: Optional[str] = None


class StageOptionCreate(StageOptionBase):
    pass


class StageOptionUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=50)
    text: Optional[str] = None
    has_diagram: Optional[bool] = None
    diagram_description: Optional[str] = None
    diagram_name: Optional[str] = None


class StageOptionRead(StageOptionBase):
    id: int
    question_id: int

    model_config = {"from_attributes": True}


# --- Stage Question Schemas ---


class StageQuestionBase(BaseModel):
    source: str = Field(..., max_length=255)
    year: str = Field(..., max_length=50)
    subject: str = Field(..., max_length=255)
    chapter: str = Field(..., max_length=255)
    topic: str = Field(..., max_length=255)
    question_number: str = Field(..., max_length=50)
    question_text: str
    has_diagram: bool = False
    diagram_description: Optional[str] = None
    diagram_position: Optional[str] = None
    diagram_name: Optional[str] = None
    answer: str = Field(..., max_length=50)
    solution: Optional[str] = None
    reviewed: bool = False


class StageQuestionCreate(StageQuestionBase):
    options: list[StageOptionCreate] = []


class StageQuestionUpdate(BaseModel):
    source: Optional[str] = Field(None, max_length=255)
    year: Optional[str] = Field(None, max_length=50)
    subject: Optional[str] = Field(None, max_length=255)
    chapter: Optional[str] = Field(None, max_length=255)
    topic: Optional[str] = Field(None, max_length=255)
    question_number: Optional[str] = Field(None, max_length=50)
    question_text: Optional[str] = None
    has_diagram: Optional[bool] = None
    diagram_description: Optional[str] = None
    diagram_position: Optional[str] = None
    diagram_name: Optional[str] = None
    answer: Optional[str] = Field(None, max_length=50)
    solution: Optional[str] = None
    reviewed: Optional[bool] = None
    options: Optional[list[StageOptionUpdate]] = None


class StageQuestionRead(StageQuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    options: list[StageOptionRead] = []

    model_config = {"from_attributes": True}
