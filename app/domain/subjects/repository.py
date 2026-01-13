from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.subjects.models import Chapter, Subject, Topic
from app.domain.subjects.schemas import (
    ChapterCreate,
    ChapterUpdate,
    SubjectCreate,
    SubjectUpdate,
    TopicCreate,
    TopicUpdate,
)


class SubjectsRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Subject Methods ---
    def create_subject(self, subject: SubjectCreate) -> Subject:
        db_subject = Subject(
            subject_name=subject.subject_name,
            no_of_questions=subject.no_of_questions,
            is_active=subject.is_active,
        )
        self.db.add(db_subject)
        self.db.flush()  # Flush to get the ID

        if subject.chapters:
            for chapter_data in subject.chapters:
                db_chapter = Chapter(
                    no=chapter_data.no,
                    name=chapter_data.name,
                    subject_id=db_subject.id,
                    formatted_name=chapter_data.formatted_name,
                    no_of_questions=chapter_data.no_of_questions,
                    is_active=chapter_data.is_active,
                )
                self.db.add(db_chapter)
                self.db.flush()

                if chapter_data.topics:
                    for topic_data in chapter_data.topics:
                        db_topic = Topic(
                            no=topic_data.no,
                            name=topic_data.name,
                            chapter_id=db_chapter.id,
                            formatted_name=topic_data.formatted_name,
                            no_of_questions=topic_data.no_of_questions,
                            is_active=topic_data.is_active,
                        )
                        self.db.add(db_topic)

        self.db.commit()
        self.db.refresh(db_subject)
        return db_subject

    def get_subject(self, subject_id: int) -> Optional[Subject]:
        return self.db.execute(
            select(Subject).where(Subject.id == subject_id)
        ).scalar_one_or_none()

    def get_subjects(self, skip: int = 0, limit: int = 100) -> Sequence[Subject]:
        return (
            self.db.execute(select(Subject).offset(skip).limit(limit)).scalars().all()
        )

    def update_subject(
        self, db_subject: Subject, subject_update: SubjectUpdate
    ) -> Subject:
        update_data = subject_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_subject, key, value)
        self.db.add(db_subject)
        self.db.commit()
        self.db.refresh(db_subject)
        return db_subject

    def delete_subject(self, db_subject: Subject) -> None:
        self.db.delete(db_subject)
        self.db.commit()

    # --- Chapter Methods ---
    def create_chapter(self, chapter: ChapterCreate) -> Chapter:
        db_chapter = Chapter(
            no=chapter.no,
            name=chapter.name,
            subject_id=chapter.subject_id,
            formatted_name=chapter.formatted_name,
            no_of_questions=chapter.no_of_questions,
            is_active=chapter.is_active,
        )
        self.db.add(db_chapter)
        self.db.flush()

        if chapter.topics:
            for topic_data in chapter.topics:
                db_topic = Topic(
                    no=topic_data.no,
                    name=topic_data.name,
                    chapter_id=db_chapter.id,
                    formatted_name=topic_data.formatted_name,
                    no_of_questions=topic_data.no_of_questions,
                    is_active=topic_data.is_active,
                )
                self.db.add(db_topic)

        self.db.commit()
        self.db.refresh(db_chapter)
        return db_chapter

    def get_chapter(self, chapter_id: int) -> Optional[Chapter]:
        return self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        ).scalar_one_or_none()

    def get_chapters_by_subject(
        self, subject_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Chapter]:
        return (
            self.db.execute(
                select(Chapter)
                .where(Chapter.subject_id == subject_id)
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )

    def update_chapter(
        self, db_chapter: Chapter, chapter_update: ChapterUpdate
    ) -> Chapter:
        update_data = chapter_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_chapter, key, value)
        self.db.add(db_chapter)
        self.db.commit()
        self.db.refresh(db_chapter)
        return db_chapter

    def delete_chapter(self, db_chapter: Chapter) -> None:
        self.db.delete(db_chapter)
        self.db.commit()

    # --- Topic Methods ---
    def create_topic(self, topic: TopicCreate) -> Topic:
        db_topic = Topic(
            no=topic.no,
            name=topic.name,
            chapter_id=topic.chapter_id,
            formatted_name=topic.formatted_name,
            no_of_questions=topic.no_of_questions,
            is_active=topic.is_active,
        )
        self.db.add(db_topic)
        self.db.commit()
        self.db.refresh(db_topic)
        return db_topic

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        return self.db.execute(
            select(Topic).where(Topic.id == topic_id)
        ).scalar_one_or_none()

    def get_topics_by_chapter(
        self, chapter_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Topic]:
        return (
            self.db.execute(
                select(Topic)
                .where(Topic.chapter_id == chapter_id)
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )

    def update_topic(self, db_topic: Topic, topic_update: TopicUpdate) -> Topic:
        update_data = topic_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_topic, key, value)
        self.db.add(db_topic)
        self.db.commit()
        self.db.refresh(db_topic)
        return db_topic

    def delete_topic(self, db_topic: Topic) -> None:
        self.db.delete(db_topic)
        self.db.commit()
