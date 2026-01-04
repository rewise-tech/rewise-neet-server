from typing import List, Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.subjects.models import Chapter, Subject, Topic
from app.domain.subjects.repository import SubjectsRepository
from app.domain.subjects.schemas import (
    ChapterCreate,
    ChapterUpdate,
    SubjectCreate,
    SubjectUpdate,
    TopicCreate,
    TopicUpdate,
)


class SubjectsService:
    def __init__(self, db: Session):
        self.repo = SubjectsRepository(db)

    # --- Subject Methods ---
    def create_subject(self, subject: SubjectCreate) -> Subject:
        return self.repo.create_subject(subject)

    def get_subject(self, subject_id: int) -> Subject:
        subject = self.repo.get_subject(subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
            )
        return subject

    def get_subjects(self, skip: int = 0, limit: int = 100) -> Sequence[Subject]:
        return self.repo.get_subjects(skip, limit)

    def update_subject(self, subject_id: int, subject_update: SubjectUpdate) -> Subject:
        db_subject = self.get_subject(subject_id)
        return self.repo.update_subject(db_subject, subject_update)

    def delete_subject(self, subject_id: int) -> None:
        db_subject = self.get_subject(subject_id)
        self.repo.delete_subject(db_subject)

    # --- Chapter Methods ---
    def create_chapter(self, chapter: ChapterCreate) -> Chapter:
        # Validate that subject exists
        self.get_subject(chapter.subject_id)
        return self.repo.create_chapter(chapter)

    def get_chapter(self, chapter_id: int) -> Chapter:
        chapter = self.repo.get_chapter(chapter_id)
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found"
            )
        return chapter

    def get_chapters_by_subject(
        self, subject_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Chapter]:
        # Validate subject exists
        self.get_subject(subject_id)
        return self.repo.get_chapters_by_subject(subject_id, skip, limit)

    def update_chapter(self, chapter_id: int, chapter_update: ChapterUpdate) -> Chapter:
        db_chapter = self.get_chapter(chapter_id)
        if chapter_update.subject_id:
            self.get_subject(chapter_update.subject_id)
        return self.repo.update_chapter(db_chapter, chapter_update)

    def delete_chapter(self, chapter_id: int) -> None:
        db_chapter = self.get_chapter(chapter_id)
        self.repo.delete_chapter(db_chapter)

    # --- Topic Methods ---
    def create_topic(self, topic: TopicCreate) -> Topic:
        # Validate chapter exists
        self.get_chapter(topic.chapter_id)
        return self.repo.create_topic(topic)

    def get_topic(self, topic_id: int) -> Topic:
        topic = self.repo.get_topic(topic_id)
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
            )
        return topic

    def get_topics_by_chapter(
        self, chapter_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Topic]:
        # Validate chapter exists
        self.get_chapter(chapter_id)
        return self.repo.get_topics_by_chapter(chapter_id, skip, limit)

    def update_topic(self, topic_id: int, topic_update: TopicUpdate) -> Topic:
        db_topic = self.get_topic(topic_id)
        if topic_update.chapter_id:
            self.get_chapter(topic_update.chapter_id)
        return self.repo.update_topic(db_topic, topic_update)

    def delete_topic(self, topic_id: int) -> None:
        db_topic = self.get_topic(topic_id)
        self.repo.delete_topic(db_topic)
