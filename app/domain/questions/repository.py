from __future__ import annotations

from typing import Optional

from sqlalchemy import Integer, cast, select
from sqlalchemy.orm import Session

from app.domain.questions.models import Question


class QuestionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Question]:
        stmt = select(Question).order_by(Question.id)
        return list(self.session.scalars(stmt))

    def list_by_year(self, year: str) -> list[Question]:
        stmt = (
            select(Question)
            .where(Question.year == year)
            .order_by(cast(Question.question_number, Integer))
        )
        return list(self.session.scalars(stmt))

    def search(
        self,
        *,
        year: Optional[str] = None,
        source: Optional[str] = None,
        subject: Optional[str] = None,
        chapter: Optional[str] = None,
        reviewed: Optional[bool] = None,
    ) -> list[Question]:
        stmt = select(Question)
        if year:
            stmt = stmt.where(Question.year == year)
        if source:
            stmt = stmt.where(Question.source == source)
        if subject:
            stmt = stmt.where(Question.subject == subject)
        if chapter:
            stmt = stmt.where(Question.chapter == chapter)
        if reviewed is not None:
            stmt = stmt.where(Question.reviewed == reviewed)

        stmt = stmt.order_by(cast(Question.question_number, Integer))
        return list(self.session.scalars(stmt))

    def get_by_question_number(
        self, *, year: str, question_number: str
    ) -> Optional[Question]:
        stmt = (
            select(Question)
            .where(
                Question.year == year,
                Question.question_number == question_number,
            )
            .order_by(Question.id)
            .limit(1)
        )
        return self.session.scalars(stmt).first()

    def get(self, question_id: int) -> Optional[Question]:
        return self.session.get(Question, question_id)

    def create(self, question: Question) -> Question:
        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def update(self, question: Question, **fields) -> Question:
        for key, value in fields.items():
            if value is not None:
                setattr(question, key, value)

        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def delete(self, question: Question) -> None:
        self.session.delete(question)
        self.session.commit()
