from sqlalchemy.orm import Session

from app.domain.questions import schemas
from app.domain.questions.models import Option, Question
from app.domain.questions.repository import QuestionRepository


class QuestionService:
    def __init__(self, session: Session) -> None:
        self.repo = QuestionRepository(session)

    def list_questions(self) -> list[Question]:
        return self.repo.list()

    def search_questions_by_year(self, year: str) -> list[Question]:
        return self.repo.list_by_year(year)

    def search_questions(
        self,
        year: str | None = None,
        source: str | None = None,
        subject: str | None = None,
        chapter: str | None = None,
        reviewed: bool | None = None,
    ) -> list[Question]:
        return self.repo.search(
            year=year,
            source=source,
            subject=subject,
            chapter=chapter,
            reviewed=reviewed,
        )

    def get_question_by_question_number(
        self, *, year: str, question_number: str
    ) -> Question | None:
        return self.repo.get_by_question_number(
            year=year, question_number=question_number
        )

    def get_question(self, question_id: int) -> Question | None:
        return self.repo.get(question_id)

    def create_question(self, payload: schemas.QuestionCreate) -> Question:
        # Create Question instance
        question = Question(
            source=payload.source,
            year=payload.year,
            subject=payload.subject,
            chapter=payload.chapter,
            topic=payload.topic,
            question_number=payload.question_number,
            question_text=payload.question_text,
            difficulty=payload.difficulty,
            has_diagram=payload.has_diagram,
            diagram_description=payload.diagram_description,
            diagram_position=payload.diagram_position,
            diagram_name=payload.diagram_name,
            answer=payload.answer,
            ai_answer=payload.ai_answer,
            solution=payload.solution,
            reviewed=payload.reviewed,
        )

        # Create Option instances and associate them
        for opt_payload in payload.options:
            option = Option(
                label=opt_payload.label,
                text=opt_payload.text,
                has_diagram=opt_payload.has_diagram,
                diagram_description=opt_payload.diagram_description,
                diagram_name=opt_payload.diagram_name,
            )
            question.options.append(option)

        return self.repo.create(question)

    def update_question(
        self, question: Question, payload: schemas.QuestionUpdate
    ) -> Question:
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
        if payload.difficulty is not None:
            fields["difficulty"] = payload.difficulty
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
        if payload.ai_answer is not None:
            fields["ai_answer"] = payload.ai_answer
        if payload.solution is not None:
            fields["solution"] = payload.solution
        if payload.reviewed is not None:
            fields["reviewed"] = payload.reviewed

        if payload.options is not None:
            for opt_payload in payload.options:
                for index, opt in enumerate(question.options):
                    if opt.id == opt_payload.id:
                        question.options[index].label = opt_payload.label
                        question.options[index].text = opt_payload.text
                        question.options[index].has_diagram = opt_payload.has_diagram
                        question.options[
                            index
                        ].diagram_description = opt_payload.diagram_description
                        question.options[index].diagram_name = opt_payload.diagram_name
                        break

        return self.repo.update(question, **fields)

    def delete_question(self, question: Question) -> None:
        self.repo.delete(question)
