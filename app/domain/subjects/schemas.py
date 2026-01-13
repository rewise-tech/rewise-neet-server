from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# --- Topic Schemas ---
class TopicBase(BaseModel):
    no: str
    name: str
    formatted_name: str
    no_of_questions: Optional[int] = None
    is_active: Optional[bool] = True


class TopicCreate(TopicBase):
    chapter_id: Optional[int] = None


class TopicUpdate(BaseModel):
    no: Optional[str] = None
    name: Optional[str] = None
    formatted_name: Optional[str] = None
    chapter_id: Optional[int] = None
    no_of_questions: Optional[int] = None
    is_active: Optional[bool] = None


class TopicResponse(TopicBase):
    id: int
    chapter_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Chapter Schemas ---
class ChapterBase(BaseModel):
    no: str
    name: str
    formatted_name: str
    no_of_questions: Optional[int] = None
    is_active: Optional[bool] = True


class ChapterCreate(ChapterBase):
    subject_id: Optional[int] = None
    topics: Optional[List[TopicCreate]] = []


class ChapterUpdate(BaseModel):
    no: Optional[str] = None
    name: Optional[str] = None
    formatted_name: Optional[str] = None
    subject_id: Optional[int] = None
    no_of_questions: Optional[int] = None
    is_active: Optional[bool] = None


class ChapterResponse(ChapterBase):
    id: int
    subject_id: int
    topics: List[TopicResponse] = []
    model_config = ConfigDict(from_attributes=True)


# --- Subject Schemas ---
class SubjectBase(BaseModel):
    subject_name: str
    no_of_questions: Optional[int] = None
    is_active: Optional[bool] = True


class SubjectCreate(SubjectBase):
    chapters: Optional[List[ChapterCreate]] = []


class SubjectUpdate(BaseModel):
    subject_name: Optional[str] = None
    no_of_questions: Optional[int] = None
    is_active: Optional[bool] = None


class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    chapters: List[ChapterResponse] = []
    model_config = ConfigDict(from_attributes=True)
