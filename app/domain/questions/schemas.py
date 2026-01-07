from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Option Schemas ---


class OptionBase(BaseModel):
    label: Optional[str] = Field(
        None, max_length=50, description="Option label like A, B, C, D"
    )
    text: Optional[str] = Field(None, description="The text content of the option")
    has_diagram: bool = False
    diagram_description: Optional[str] = None
    diagram_name: Optional[str] = None


class OptionCreate(OptionBase):
    pass


class OptionUpdate(BaseModel):
    id: int
    label: Optional[str] = Field(None, max_length=50)
    text: Optional[str] = None
    has_diagram: Optional[bool] = None
    diagram_description: Optional[str] = None
    diagram_name: Optional[str] = None


class OptionRead(OptionBase):
    id: int
    question_id: int

    model_config = {"from_attributes": True}


# --- Question Schemas ---


class QuestionBase(BaseModel):
    source: Optional[str] = Field(None, max_length=255)
    year: Optional[str] = Field(None, max_length=50)
    subject: Optional[str] = Field(None, max_length=255)
    chapter: Optional[str] = Field(None, max_length=255)
    topic: Optional[str] = Field(None, max_length=255)
    question_number: str = Field(..., max_length=50)
    question_text: Optional[str] = None
    difficulty: Optional[str] = None
    has_diagram: bool = False
    diagram_description: Optional[str] = None
    diagram_position: Optional[str] = None
    diagram_name: Optional[str] = None
    answer: Optional[str] = Field(None, max_length=50)
    ai_answer: Optional[str] = None
    solution: Optional[str] = None
    reviewed: bool = False


class QuestionCreate(QuestionBase):
    options: list[OptionCreate] = []


class QuestionUpdate(BaseModel):
    id: int
    source: Optional[str] = Field(None, max_length=255)
    year: Optional[str] = Field(None, max_length=50)
    subject: Optional[str] = Field(None, max_length=255)
    chapter: Optional[str] = Field(None, max_length=255)
    topic: Optional[str] = Field(None, max_length=255)
    question_number: Optional[str] = Field(None, max_length=50)
    question_text: Optional[str] = None
    difficulty: Optional[str] = None
    has_diagram: Optional[bool] = None
    diagram_description: Optional[str] = None
    diagram_position: Optional[str] = None
    diagram_name: Optional[str] = None
    answer: Optional[str] = Field(None, max_length=50)
    ai_answer: Optional[str] = None
    solution: Optional[str] = None
    reviewed: Optional[bool] = None
    options: Optional[list[OptionUpdate]] = None


class QuestionSearchRead(BaseModel):
    id: int
    source: Optional[str]
    year: Optional[str]
    subject: Optional[str]
    chapter: Optional[str]
    question_number: str
    question_text: Optional[str] = None
    reviewed: bool
    answer: Optional[str]
    ai_answer: Optional[str]
    solution: Optional[str]
    options: Optional[list[OptionRead]] = None

    model_config = {"from_attributes": True}


class QuestionRead(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    ai_answer: Optional[str] = None
    options: list[OptionRead] = []

    model_config = {"from_attributes": True}
