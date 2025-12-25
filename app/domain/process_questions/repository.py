from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.process_questions.models import StageQuestion


class StageQuestionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[StageQuestion]:
        stmt = select(StageQuestion).order_by(StageQuestion.id)
        return list(self.session.scalars(stmt))

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
