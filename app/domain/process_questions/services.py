from sqlalchemy.orm import Session

from app.domain.process_questions import schemas
from app.domain.process_questions.models import StageOption, StageQuestion
from app.domain.process_questions.repository import StageQuestionRepository


class StageQuestionService:
    def __init__(self, session: Session) -> None:
        self.repo = StageQuestionRepository(session)

    def list_questions(self) -> list[StageQuestion]:
        return self.repo.list()

    def search_questions_by_year(self, year: str) -> list[StageQuestion]:
        return self.repo.list_by_year(year)

    def get_question_by_question_number(
        self, *, year: str, question_number: str
    ) -> StageQuestion | None:
        return self.repo.get_by_question_number(
            year=year, question_number=question_number
        )

    def get_question(self, question_id: int) -> StageQuestion | None:
        return self.repo.get(question_id)

    def create_question(self, payload: schemas.StageQuestionCreate) -> StageQuestion:
        # Create StageQuestion instance
        question = StageQuestion(
            source=payload.source,
            year=payload.year,
            subject=payload.subject,
            chapter=payload.chapter,
            topic=payload.topic,
            question_number=payload.question_number,
            question_text=payload.question_text,
            has_diagram=payload.has_diagram,
            diagram_description=payload.diagram_description,
            diagram_position=payload.diagram_position,
            diagram_name=payload.diagram_name,
            answer=payload.answer,
            solution=payload.solution,
            reviewed=payload.reviewed,
        )

        # Create StageOption instances and associate them
        for opt_payload in payload.options:
            option = StageOption(
                label=opt_payload.label,
                text=opt_payload.text,
                has_diagram=opt_payload.has_diagram,
                diagram_description=opt_payload.diagram_description,
                diagram_name=opt_payload.diagram_name,
            )
            question.options.append(option)

        return self.repo.create(question)

    def update_question(
        self, question: StageQuestion, payload: schemas.StageQuestionUpdate
    ) -> StageQuestion:
        fields: dict[str, object] = {}
        if payload.source is not None:
            fields["source"] = payload.source
        if payload.year is not None:
            fields["year"] = payload.year
        if payload.subject is not None:
            fields["subject"] = payload.subject
        if payload.chapter is not None:
            fields["chapter"] = payload.chapter
        if payload.topic is not None:
            fields["topic"] = payload.topic
        if payload.question_number is not None:
            fields["question_number"] = payload.question_number
        if payload.question_text is not None:
            fields["question_text"] = payload.question_text
        if payload.has_diagram is not None:
            fields["has_diagram"] = payload.has_diagram
        if payload.diagram_description is not None:
            fields["diagram_description"] = payload.diagram_description
        if payload.diagram_position is not None:
            fields["diagram_position"] = payload.diagram_position
        if payload.diagram_name is not None:
            fields["diagram_name"] = payload.diagram_name
        if payload.answer is not None:
            fields["answer"] = payload.answer
        if payload.solution is not None:
            fields["solution"] = payload.solution
        if payload.reviewed is not None:
            fields["reviewed"] = payload.reviewed

        # Note: Nested option updates are not fully implemented here as they require
        # a strategy for reconciling existing vs new options (add/remove/update).
        # For this iteration, we focus on updating top-level fields.

        return self.repo.update(question, **fields)

    def delete_question(self, question: StageQuestion) -> None:
        self.repo.delete(question)
