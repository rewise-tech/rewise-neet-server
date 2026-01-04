from __future__ import annotations

from typing import Optional

from sqlalchemy import Integer, cast, select
from sqlalchemy.orm import Session

from app.domain.process_questions.models import StageQuestion


class StageQuestionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[StageQuestion]:
        stmt = select(StageQuestion).order_by(StageQuestion.id)
        return list(self.session.scalars(stmt))

    def search(
        self,
        *,
        year: Optional[str] = None,
        source: Optional[str] = None,
        subject: Optional[str] = None,
        chapter: Optional[str] = None,
        reviewed: Optional[bool] = None,
    ) -> list[StageQuestion]:
        stmt = select(StageQuestion)
        if year:
            stmt = stmt.where(StageQuestion.year == year)
        if source:
            stmt = stmt.where(StageQuestion.source == source)
        if subject:
            stmt = stmt.where(StageQuestion.subject == subject)
        if chapter:
            stmt = stmt.where(StageQuestion.chapter == chapter)
        if reviewed is not None:
            stmt = stmt.where(StageQuestion.reviewed == reviewed)

        stmt = stmt.order_by(cast(StageQuestion.question_number, Integer))
        return list(self.session.scalars(stmt))

    def get_by_question_number(
        self, *, year: str, question_number: str
    ) -> Optional[StageQuestion]:
        stmt = (
            select(StageQuestion)
            .where(
                StageQuestion.year == year,
                StageQuestion.question_number == question_number,
            )
            .order_by(StageQuestion.id)
            .limit(1)
        )
        return self.session.scalars(stmt).first()

    def get(self, question_id: int) -> Optional[StageQuestion]:
        return self.session.get(StageQuestion, question_id)

    def create(self, question: StageQuestion) -> StageQuestion:
        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def update(self, question: StageQuestion, **fields) -> StageQuestion:
        for key, value in fields.items():
            if value is not None:
                setattr(question, key, value)

        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def delete(self, question: StageQuestion) -> None:
        self.session.delete(question)
        self.session.commit()

    def get_distinct_sources(self) -> list[str]:
        stmt = (
            select(StageQuestion.source)
            .distinct()
            .where(StageQuestion.source.is_not(None))
        )
        return list(self.session.scalars(stmt))

    def get_distinct_subjects(self) -> list[str]:
        stmt = (
            select(StageQuestion.subject)
            .distinct()
            .where(StageQuestion.subject.is_not(None))
        )
        return list(self.session.scalars(stmt))

    def get_distinct_chapters(self, subject: Optional[str] = None) -> list[str]:
        stmt = (
            select(StageQuestion.chapter)
            .distinct()
            .where(StageQuestion.chapter.is_not(None))
        )
        if subject:
            stmt = stmt.where(StageQuestion.subject == subject)
        return list(self.session.scalars(stmt))

    def get_distinct_years(self) -> list[str]:
        stmt = (
            select(StageQuestion.year).distinct().where(StageQuestion.year.is_not(None))
        )
        return list(self.session.scalars(stmt))
