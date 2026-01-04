from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domain.subjects.schemas import (
    ChapterCreate,
    ChapterResponse,
    ChapterUpdate,
    SubjectCreate,
    SubjectResponse,
    SubjectUpdate,
    TopicCreate,
    TopicResponse,
    TopicUpdate,
)
from app.domain.subjects.services import SubjectsService

router = APIRouter()


def get_service(db: Session = Depends(get_session)) -> SubjectsService:
    return SubjectsService(db)


# --- Subjects Routes ---
@router.post("/subjects/", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate, service: SubjectsService = Depends(get_service)
):
    return service.create_subject(subject)


@router.get("/subjects/", response_model=List[SubjectResponse])
def get_subjects(
    skip: int = 0,
    limit: int = 100,
    service: SubjectsService = Depends(get_service),
):
    return service.get_subjects(skip=skip, limit=limit)


@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, service: SubjectsService = Depends(get_service)):
    return service.get_subject(subject_id)


@router.put("/subjects/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    service: SubjectsService = Depends(get_service),
):
    return service.update_subject(subject_id, subject_update)


@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, service: SubjectsService = Depends(get_service)):
    service.delete_subject(subject_id)
    return {"ok": True}


# --- Chapters Routes ---
@router.post("/subjects/{subject_id}/chapters", response_model=ChapterResponse)
def create_chapter(
    subject_id: int,
    chapter: ChapterCreate,
    service: SubjectsService = Depends(get_service),
):
    # Ensure subject_id matches
    chapter.subject_id = subject_id
    return service.create_chapter(chapter)


@router.get("/subjects/{subject_id}/chapters", response_model=List[ChapterResponse])
def get_chapters_by_subject(
    subject_id: int,
    skip: int = 0,
    limit: int = 100,
    service: SubjectsService = Depends(get_service),
):
    return service.get_chapters_by_subject(subject_id, skip, limit)


@router.get("/chapters/{chapter_id}", response_model=ChapterResponse)
def get_chapter(chapter_id: int, service: SubjectsService = Depends(get_service)):
    return service.get_chapter(chapter_id)


@router.put("/chapters/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
    chapter_id: int,
    chapter_update: ChapterUpdate,
    service: SubjectsService = Depends(get_service),
):
    return service.update_chapter(chapter_id, chapter_update)


@router.delete("/chapters/{chapter_id}")
def delete_chapter(chapter_id: int, service: SubjectsService = Depends(get_service)):
    service.delete_chapter(chapter_id)
    return {"ok": True}


# --- Topics Routes ---
@router.post("/chapters/{chapter_id}/topics", response_model=TopicResponse)
def create_topic(
    chapter_id: int,
    topic: TopicCreate,
    service: SubjectsService = Depends(get_service),
):
    # Ensure chapter_id matches
    topic.chapter_id = chapter_id
    return service.create_topic(topic)


@router.get("/chapters/{chapter_id}/topics", response_model=List[TopicResponse])
def get_topics_by_chapter(
    chapter_id: int,
    skip: int = 0,
    limit: int = 100,
    service: SubjectsService = Depends(get_service),
):
    return service.get_topics_by_chapter(chapter_id, skip, limit)


@router.get("/topics/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, service: SubjectsService = Depends(get_service)):
    return service.get_topic(topic_id)


@router.put("/topics/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    topic_update: TopicUpdate,
    service: SubjectsService = Depends(get_service),
):
    return service.update_topic(topic_id, topic_update)


@router.delete("/topics/{topic_id}")
def delete_topic(topic_id: int, service: SubjectsService = Depends(get_service)):
    service.delete_topic(topic_id)
    return {"ok": True}
