from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.questions.models import Question


class QuestionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Question]:
        stmt = select(Question).order_by(Question.id)
        return list(self.session.scalars(stmt))

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

        # Explicitly handle options if needed, but simple attribute update is handled here.
        # Nested option updates usually require service-level coordination or specific logic
        # but basic field updates work this way for the parent object.

        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def delete(self, question: Question) -> None:
        self.session.delete(question)
        self.session.commit()
